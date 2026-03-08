# Δημιούργησε ένα νέο, σωστό database.py
@'
# database.py (SQLite έκδοση)
import sqlite3
import os
from config import Config


class Database:
    @staticmethod
    def get_connection():
        """Επιστρέφει σύνδεση με SQLite database."""
        db_path = os.path.join(os.path.dirname(__file__), "health_certificates.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def create_tables():
        """Δημιουργεί τους απαραίτητους πίνακες."""
        conn = Database.get_connection()

        try:
            cur = conn.cursor()  # 🔽 ΑΛΛΑΓΗ: Χωρίς with
            # Ενεργοποίηση foreign keys
            cur.execute("PRAGMA foreign_keys = ON")

            # Πίνακας χρηστών
            cur.execute("""
                      CREATE TABLE IF NOT EXISTS users (
                          id TEXT PRIMARY KEY,
                          username TEXT UNIQUE NOT NULL,
                          password_hash TEXT NOT NULL,
                          full_name TEXT,
                          role TEXT NOT NULL CHECK(role IN ('doctor', 'admin')),
                          is_active BOOLEAN DEFAULT 1,
                          is_default_admin BOOLEAN DEFAULT 0,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )
                  """)

            # Πίνακας πιστοποιητικών
            cur.execute("""
                CREATE TABLE IF NOT EXISTS health_certificates (
                    id TEXT PRIMARY KEY,
                    protocol_number TEXT NOT NULL,
                    proto_year INTEGER,
                    proto_seq INTEGER,
                    hc_first_name TEXT NOT NULL,
                    hc_last_name TEXT NOT NULL,
                    hc_father_name TEXT,
                    hc_amka TEXT UNIQUE,
                    hc_personal_number TEXT UNIQUE,
                    id_number TEXT,
                    passport_number TEXT,
                    certificate_date DATE NOT NULL,
                    residence TEXT NOT NULL,
                    work_type TEXT NOT NULL,
                    comments TEXT,
                    doctor_id TEXT REFERENCES users(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(protocol_number, doctor_id)
                )
            """)

            # Πίνακας συνημμένων
            cur.execute("""
                CREATE TABLE IF NOT EXISTS health_certificate_documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    certificate_id TEXT REFERENCES health_certificates(id) ON DELETE CASCADE,
                    file_name TEXT NOT NULL,
                    file_path TEXT NOT NULL UNIQUE,
                    file_size INTEGER,
                    file_type TEXT,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    doctor_id TEXT REFERENCES users(id)
                )
            """)

            # Προεπιλεγμένος χρήστης (ΣΧΟΛΙΑΣΜΕΝΟ)
            # cur.execute("""
            #     INSERT OR IGNORE INTO users (id, username, password_hash, full_name, role)
            #     VALUES ('1', 'doctor', '1234', 'Γιατρός', 'doctor')
            # """)

            conn.commit()
            print("✅ Οι πίνακες δημιουργήθηκαν επιτυχώς")
            return True

        except Exception as e:
            print(f"Σφάλμα δημιουργίας πινάκων: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    @staticmethod
    def create_default_admin():
        """Δημιουργεί τον προεπιλεγμένο διαχειριστή αν δεν υπάρχει."""
        conn = Database.get_connection()
        if not conn:
            return False

        try:
            cur = conn.cursor()

            # Έλεγχος αν υπάρχει ήδη ο προεπιλεγμένος admin
            cur.execute("SELECT COUNT(*) FROM users WHERE username = 'admin' AND COALESCE(is_default_admin, 0) = 1")
            default_admin_exists = cur.fetchone()[0] > 0

            if not default_admin_exists:
                # Δημιουργούμε τον προεπιλεγμένο admin με flag
                cur.execute("""
                    INSERT OR IGNORE INTO users 
                    (id, username, password_hash, role, is_active, is_default_admin)
                    VALUES 
                    ('11111111-1111-1111-1111-111111111111', 'admin', 'admin123', 'admin', 1, 1)
                """)
                conn.commit()
                print("✅ Δημιουργήθηκε ο προεπιλεγμένος διαχειριστής admin")
                return True
            else:
                print("ℹ️ Ο προεπιλεγμένος διαχειριστής admin υπάρχει ήδη")
                return False

        except Exception as e:
            print(f"Σφάλμα δημιουργίας προεπιλεγμένου admin: {e}")
            import traceback
            traceback.print_exc()
            return False
                
    @staticmethod
    def setup_directories():
        """Δημιουργεί τους απαραίτητους φακέλους."""
        directories = [
            Config.ATTACHMENTS_DIR,
            Config.EXPORTS_DIR,
            os.path.join(Config.ATTACHMENTS_DIR, "health_certificates")
        ]

        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Φάκελος: {directory}")
'@ | Out-File -FilePath "database_fixed.py" -Encoding UTF8

# Αντιγραφή στο σωστό όνομα
Copy-Item -Path "database_fixed.py" -Destination "database.py" -Force
Remove-Item -Path "database_fixed.py"

Write-Host "✅ Το database.py επαναφέρθηκε!"