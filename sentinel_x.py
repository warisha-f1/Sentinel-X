import sqlite3
from datetime import datetime
import time
import random
import uuid
from prefect import flow, task, pause_flow_run

# --- STATE MANAGEMENT: Generate Session ID ---
SESSION_ID = f"SES-{uuid.uuid4().hex[:6].upper()}-{datetime.now().strftime('%m%d')}"

@task
def live_researcher_agent(source_name: str):
    val = random.randint(100, 999)
    return {"source": source_name, "value": val}

@task
def aggregator_agent(results):
    summary = " | ".join([f"{r['source']}: {r['value']}" for r in results])
    avg_val = sum([r['value'] for r in results]) / len(results)
    return {"summary": summary, "avg_score": avg_val}

@task
def judge_agent(payload):
    # Agent Evaluation Logic
    print(f"⚖️ [JUDGE] Evaluating Session {SESSION_ID} (Score: {payload['avg_score']})...")
    if payload['avg_score'] > 300:
        return {"eval": "✅ HIGH QUALITY", "pause": True}
    return {"eval": "⚠️ LOW QUALITY", "pause": False}

@task
def lead_reporter_agent(payload, judgment):
    # A2A Protocol Handshake
    return (f"--- SESSION: {SESSION_ID} ---\n"
            f"JUDGE: {judgment}\n"
            f"DATA: {payload['summary']}\n"
            f"TS: {datetime.now()}\n"
            f"---------------------------")

@task
def save_to_memory(briefing):
    conn = sqlite3.connect('capstone.db')
    cursor = conn.cursor()
    # SAFETY CHECK: Ensuring the column exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS memory_bank 
                     (id INTEGER PRIMARY KEY, session_id TEXT, briefing TEXT, saved_at TEXT)''')
    
    # Writing the state to Long-Term Memory
    cursor.execute("INSERT INTO memory_bank (session_id, briefing, saved_at) VALUES (?, ?, ?)", 
                   (SESSION_ID, briefing, str(datetime.now())))
    conn.commit()
    conn.close()
    print(f"💾 [LTM] Session {SESSION_ID} persisted successfully.")

@flow(name="Sentinel-X_Session_Flow")
def sentinel_x_flow():
    print(f"🚀 STARTING SESSION: {SESSION_ID}")
    while True:
        res_a = live_researcher_agent.submit("Crypto")
        res_b = live_researcher_agent.submit("Stock")
        
        payload = aggregator_agent([res_a.result(), res_b.result()])
        judgment = judge_agent(payload)

        if judgment["pause"]:
            print(f"Wait for human in Prefect UI for session {SESSION_ID}...")
            try:
                pause_flow_run(timeout=120) 
                briefing = lead_reporter_agent(payload, judgment["eval"])
                save_to_memory(briefing)
            except Exception:
                print("🕒 Approval Timeout.")
        else:
            print("⏭️ Auto-skipping low-signal cycle.")

        time.sleep(20)

if __name__ == "__main__":
    sentinel_x_flow()