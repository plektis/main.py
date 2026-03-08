# recreate_tables.py
from database import recreate_tables

print("🔄 ΕΠΑΝΑΔΗΜΙΟΥΡΓΙΑ ΠΙΝΑΚΩΝ")
print("⚠️  Προσοχή: Αυτό θα διαγράψει όλα τα υπάρχοντα δεδομένα!")
print("=" * 40)

response = input("Θέλετε να συνεχίσετε; (ναι/όχι): ")

if response.lower() in ['ναι', 'yes', 'y', 'ν']:
    print("🔨 Διαγραφή παλιών πινάκων...")
    if recreate_tables():
        print("✅ Οι πίνακες δημιουργήθηκαν εκ νέου")
        print("🔑 Admin χρήστης: admin / admin123")
    else:
        print("❌ Κάτι πήγε στραβά")
else:
    print("❌ Ακύρωση")
