import sqlite3

def view_ltm():
    conn = sqlite3.connect('capstone.db')
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("SENTINEL-X: MULTI-SESSION MEMORY BANK")
    print("="*60)

    try:
        # Querying with Session ID awareness
        cursor.execute("SELECT session_id, briefing, saved_at FROM memory_bank ORDER BY saved_at DESC")
        rows = cursor.fetchall()
        
        for row in rows:
            print(f"\nSESSION: {row[0]}")
            print(f"DATE: {row[2]}")
            print(f"CONTENT:\n{row[1]}")
            print("-" * 60)
                
    except Exception as e:
        print(f"Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    view_ltm()