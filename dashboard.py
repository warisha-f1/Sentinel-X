import sqlite3
from collections import Counter

def run_global_dashboard():
    conn = sqlite3.connect('capstone.db')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("📊 SENTINEL-X GLOBAL CAPSTONE DASHBOARD")
    print("="*60)

    try:
        # 1. METRICS: Total Intelligence Gathered
        cursor.execute("SELECT COUNT(*) FROM memory_bank")
        total_records = cursor.fetchone()[0]
        
        # 2. STATE MANAGEMENT: Unique Sessions Tracked
        cursor.execute("SELECT COUNT(DISTINCT session_id) FROM memory_bank")
        total_sessions = cursor.fetchone()[0]
        
        # 3. AGENT EVALUATION: Analyze Judge Sentiments
        cursor.execute("SELECT briefing FROM memory_bank")
        all_briefings = cursor.fetchall()
        
        high_quality_count = sum(1 for b in all_briefings if "HIGH QUALITY" in b[0])
        
        # 4. DATA OBSERVABILITY: Identify the most active data sources
        all_text = " ".join([b[0] for b in all_briefings])
        sources = []
        if "Crypto" in all_text: sources.append("Crypto")
        if "Stock" in all_text: sources.append("Stock")

        # --- DISPLAY RESULTS ---
        print(f"📈 TOTAL RECORDS SAVED:    {total_records}")
        print(f"🆔 UNIQUE SESSIONS:        {total_sessions}")
        print(f"⚖️ HIGH-QUALITY REPORTS:   {high_quality_count}")
        print(f"🛰️ ACTIVE DATA SOURCES:    {', '.join(set(sources))}")
        print("-" * 60)
        
        # Show the most recent session's activity
        cursor.execute("SELECT session_id, saved_at FROM memory_bank ORDER BY saved_at DESC LIMIT 1")
        last = cursor.fetchone()
        if last:
            print(f"⏱️ LAST ACTIVITY: Session {last[0]} at {last[1]}")

    except Exception as e:
        print(f"❌ Dashboard Error: {e}")
        print("Ensure you have run the agents and approved at least one cycle!")
    
    conn.close()
    print("="*60 + "\n")

if __name__ == "__main__":
    run_global_dashboard()