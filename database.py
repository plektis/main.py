# database.py (PostgreSQL έκδοση διορθωμένη)
import psycopg2
from psycopg2 import sql
import os
import uuid
from config import Config
import sqlite3

class Database:

    _connection = None

    @staticmethod
    def get_connection():
        if Database._connection is None:

            db_path = os.path.join(
                os.path.dirname(__file__),
                "health_certificates.db"
            )

            Database._connection = sqlite3.connect(db_path)
            Database._connection.row_factory = sqlite3.Row

        return Database._connection

    @staticmethod
    def create_tables():
        """Δημιουργεί τους απαραίτητους πίνακες."""
        conn = Database.get_connection()
        if not conn:
            return False

        try:
            cur = conn.cursor()

            # Πίνακας χρηστών - ΜΕ is_default_admin
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(36) PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL CHECK(role IN ('doctor', 'admin')),
                    is_active BOOLEAN DEFAULT TRUE,
                    is_default_admin BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Πίνακας πιστοποιητικών
            cur.execute("""
                CREATE TABLE IF NOT EXISTS health_certificates (
                    id VARCHAR(36) PRIMARY KEY,
                    protocol_number VARCHAR(50) NOT NULL,
                    proto_year INTEGER,
                    proto_seq INTEGER,
                    hc_first_name VARCHAR(100) NOT NULL,
                    hc_last_name VARCHAR(100) NOT NULL,
                    hc_father_name VARCHAR(100),
                    hc_amka VARCHAR(11) UNIQUE,
                    hc_personal_number VARCHAR(12) UNIQUE,
                    id_number VARCHAR(50),
                    passport_number VARCHAR(50),
                    certificate_date DATE NOT NULL,
                    residence TEXT NOT NULL,
                    work_type VARCHAR(100) NOT NULL,
                    comments TEXT,
                    doctor_id VARCHAR(36) REFERENCES users(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(protocol_number, doctor_id)
                )
            """)

            # Πίνακας συνημμένων
            cur.execute("""
                CREATE TABLE IF NOT EXISTS health_certificate_documents (
                    id SERIAL PRIMARY KEY,
                    certificate_id VARCHAR(36) REFERENCES health_certificates(id) ON DELETE CASCADE,
                    file_name VARCHAR(255) NOT NULL,
                    file_path TEXT NOT NULL UNIQUE,
                    file_size INTEGER,
                    file_type VARCHAR(50),
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    doctor_id VARCHAR(36) REFERENCES users(id)
                )
            """)

            conn.commit()
            print("✅ Οι πίνακες δημιουργήθηκαν επιτυχώς")
            return True

        except Exception as e:
            print(f"❌ Σφάλμα δημιουργίας πινάκων: {e}")
            conn.rollback()
            return False

    @staticmethod
    def create_default_admin():
        """Δημιουργεί τον προεπιλεγμένο διαχειριστή."""
        conn = Database.get_connection()
        if not conn:
            return False

        try:
            cur = conn.cursor()

            # Έλεγχος αν υπάρχει ήδη admin (ΧΩΡΙΣ is_default_admin για συμβατότητα)
            cur.execute("""
                SELECT COUNT(*) FROM users WHERE username = 'admin'
            """)
            admin_exists = cur.fetchone()[0] > 0

            if not admin_exists:
                cur.execute("""
                    INSERT INTO users 
                    (id, username, password_hash, role, is_active, is_default_admin)
                    VALUES 
                    (%s, 'admin', 'admin123', 'admin', TRUE, TRUE)
                    ON CONFLICT (username) DO NOTHING
                """, ('11111111-1111-1111-1111-111111111111',))
                
                conn.commit()
                print("✅ Δημιουργήθηκε ο διαχειριστής admin")
                return True
            else:
                print("ℹ️ Ο διαχειριστής admin υπάρχει ήδη")
                return False

        except Exception as e:
            print(f"❌ Σφάλμα: {e}")
            conn.rollback()
            return False

    @staticmethod
    def setup_backup_directory():
        """Δημιουργεί τον φάκελο για backups."""
        backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        print(f"📁 Φάκελος backup: {backup_dir}")
        return backup_dir

    @staticmethod
    def setup_directories():
        """Δημιουργεί τους απαραίτητους φακέλους."""
        Config.setup_directories()


# Βοηθητική συνάρτηση για επανάληψη δημιουργίας πινάκων
def recreate_tables():
    """Διαγράφει και ξαναδημιουργεί τους πίνακες (ΧΡΗΣΗ ΜΕ ΠΡΟΣΟΧΗ!)."""
    conn = Database.get_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        
        # Διαγραφή πινάκων (σε σωστή σειρά λόγω foreign keys)
        cur.execute("DROP TABLE IF EXISTS health_certificate_documents CASCADE")
        cur.execute("DROP TABLE IF EXISTS health_certificates CASCADE")
        cur.execute("DROP TABLE IF EXISTS users CASCADE")
        
        conn.commit()
        print("🗑️  Οι παλιοί πίνακες διαγράφηκαν")
        
        # Δημιουργία νέων πινάκων
        return Database.create_tables()
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Σφάλμα: {e}")
        return False
    