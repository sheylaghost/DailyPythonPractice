import os
import re
import json
import datetime
from collections import defaultdict

# --- Configurações (Mantidas para a lógica) ---
LOG_DIR = "./sample_logs_minimal" # Novo diretório para não misturar
DEAD_LETTER_FILE = "dead_letters_minimal.log"
WINDOW_SIZE_SECONDS = 5 * 60  # 5 minutos
CHUNK_TARGET_SIZE = 5         # Ajustado para forçar a visibilidade
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S" 
LOG_REGEX = re.compile(r"^\[(?P<timestamp>.*?)\] \[(?P<service>.*?)\] \[(?P<level>.*?)\] (?P<message>.*)$")

# --- Funções de Pipeline (Não Alteradas, Apenas Copiadas) ---

def epoch_to_datetime_obj(entry):
    """Converte o timestamp Epoch de volta para o objeto datetime para a saída estética."""
    entry['timestamp'] = datetime.datetime.fromtimestamp(entry['timestamp'])
    return entry

# FUNÇÃO 1: Varredura (Simplificada)
def log_scanner(log_directory):
    for root, _, files in os.walk(log_directory):
        for file_name in files:
            if file_name.endswith(".log"):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            yield line.strip()
                except IOError:
                    pass

# FUNÇÃO 2: Normalização (Usa Epoch Time)
def normalize_entry(log_line_generator):
    def write_to_dead_letter(line):
        with open(DEAD_LETTER_FILE, 'a', encoding='utf-8') as dl:
            dl.write(f"{datetime.datetime.now().isoformat()} | Malformed Log: {line}\n")
    
    for line in log_line_generator:
        try:
            match = LOG_REGEX.match(line)
            if not match: raise ValueError()
            data = match.groupdict()
            dt_obj = datetime.datetime.strptime(data['timestamp'], TIMESTAMP_FORMAT)
            timestamp_epoch = int(dt_obj.timestamp())
            yield {
                "timestamp": timestamp_epoch,
                "service": data.get('service', 'UNKNOWN'),
                "level": data.get('level', 'DEBUG'),
                "message": data.get('message', ''),
                "meta": {}
            }
        except Exception:
            write_to_dead_letter(line)

# FUNÇÃO 3: Agrupamento
def group_by_window(normalized_entries_generator, window_size_sec):
    window_buffer = defaultdict(list)
    oldest_window_key = None 

    for entry in normalized_entries_generator:
        ts = entry['timestamp']
        window_key = ts // window_size_sec
        
        if oldest_window_key is None: oldest_window_key = window_key

        if window_key > oldest_window_key:
            keys_to_close = sorted([k for k in window_buffer.keys() if k < window_key])
            for key in keys_to_close:
                yield window_buffer.pop(key)
            oldest_window_key = window_key
            
        window_buffer[window_key].append(entry)

    for key in sorted(window_buffer.keys()):
        yield window_buffer[key]
        
# FUNÇÃO 4: Chunking (Converte para objeto datetime na saída)
def chunk_windows(closed_windows_generator, chunk_target_size):
    current_chunk_epoch = []
    
    for window_entries in closed_windows_generator:
        
        if len(current_chunk_epoch) + len(window_entries) < chunk_target_size:
            current_chunk_epoch.extend(window_entries)
        else:
            if current_chunk_epoch:
                yield [epoch_to_datetime_obj(e.copy()) for e in current_chunk_epoch]
                current_chunk_epoch = []
                
            if len(window_entries) >= chunk_target_size:
                for i in range(0, len(window_entries), chunk_target_size):
                    sub_chunk_epoch = window_entries[i:i + chunk_target_size]
                    yield [epoch_to_datetime_obj(e.copy()) for e in sub_chunk_epoch]
            else:
                current_chunk_epoch.extend(window_entries)

    if current_chunk_epoch:
        yield [epoch_to_datetime_obj(e.copy()) for e in current_chunk_epoch]

# ==============================================================================
# 3. Execução Principal e Demonstração MINIMALISTA
# ==============================================================================

def run_pipeline():
    """Cria dados de amostra e executa o pipeline, exibindo apenas o primeiro chunk."""
    
    # Setup de diretório e limpeza
    if not os.path.exists(LOG_DIR): os.makedirs(LOG_DIR)
    if os.path.exists(DEAD_LETTER_FILE): os.remove(DEAD_LETTER_FILE)
        
    dt_base = datetime.datetime(2025, 10, 31, 15, 0, 0)
    def format_log(dt, service, level, msg):
        return f"[{dt.strftime(TIMESTAMP_FORMAT)}] [{service}] [{level}] {msg}"

    # Dados de amostra para caberem em 1 chunk (~5 logs)
    logs_file_small = [
        format_log(dt_base + datetime.timedelta(seconds=10), "ServiceA", "INFO", "User logged in: user123"),
        format_log(dt_base + datetime.timedelta(seconds=20), "ServiceB", "ERROR", "Payment failed", ),
        format_log(dt_base + datetime.timedelta(seconds=35), "ServiceC", "WARN", "Disk usage high: 87%", ),
        "LINHA MALFORMADA PARA DEAD LETTER", # 1 Dead Letter
        format_log(dt_base + datetime.timedelta(seconds=55), "ServiceA", "DEBUG", "Heartbeat received"), 
    ]
    
    with open(os.path.join(LOG_DIR, "small_logs.log"), 'w') as f: 
        f.write('\n'.join(logs_file_small))
    
    print(">>> Pipeline Minimalista: Exibindo Apenas o Primeiro Chunk (Target Size: 5) <<<")
    
    # 2. Montagem da Pipeline
    line_generator = log_scanner(LOG_DIR)
    normalized_generator = normalize_entry(line_generator)
    window_generator = group_by_window(normalized_generator, WINDOW_SIZE_SECONDS)
    chunk_generator = chunk_windows(window_generator, CHUNK_TARGET_SIZE)

    # 3. Consumo Minimalista (Apenas o primeiro item)
    try:
        first_chunk = next(chunk_generator)
        
        print("\n--- Chunk #1 Exemplo Minimalista ---")
        print('[')
        
        # Imprime cada entrada do chunk no formato estético
        for entry in first_chunk:
            # Substitui as aspas simples de ditc python por duplas para se assemelhar mais ao JSON
            print(str(entry).replace("'", '"')) 
        print(']')
        
        print(f"\n✅ Total de Entradas no Chunk: {len(first_chunk)}")
        
    except StopIteration:
        print("AVISO: Nenhum chunk foi produzido.")

    print(f"Malformadas em: {DEAD_LETTER_FILE}")

# Execução do desafio
if __name__ == '__main__':
    run_pipeline()