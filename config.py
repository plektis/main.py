# config.py (PostgreSQL έκδοση)
import os

class Config:
    # Ονομασία εφαρμογής
    APP_NAME = "Σύστημα Πιστοποιητικών Υγείας"
    APP_VERSION = "1.0.0"
    
    # ⚠️ ΑΛΛΑΞΕ ΑΥΤΕΣ ΤΙΣ ΤΙΜΕΣ ΜΕ ΤΑ ΣΤΟΙΧΕΙΑ ΣΟΥ ⚠️
    DB_HOST = "localhost"                 # Συνήθως localhost
    DB_PORT = "5432"                      # Προεπιλεγμένη θύρα PostgreSQL
    DB_NAME = "health_certificates_db"    # Όνομα βάσης στο pgAdmin4
    DB_USER = "postgres"                  # Το username σου
    DB_PASSWORD = "lag700701"   # ΚΩΔΙΚΟΣ ΠΡΟΣΟΧΗ!
    
    # File paths (παραμένουν ίδια)
    ATTACHMENTS_DIR = "attachments"
    EXPORTS_DIR = "exports"
    
    @classmethod
    def get_db_config(cls):
        """Επιστρέφει τη διαμόρφωση PostgreSQL."""
        return {
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "database": cls.DB_NAME,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD
        }
    
    @classmethod
    def setup_directories(cls):
        """Δημιουργεί τους απαραίτητους φακέλους."""
        directories = [
            cls.ATTACHMENTS_DIR,
            cls.EXPORTS_DIR,
            os.path.join(cls.ATTACHMENTS_DIR, "health_certificates")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Φάκελος: {directory}")
