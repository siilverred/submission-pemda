from utils.extract import scrape_all
from utils.transform import transform
from utils.load import load_to_csv, load_to_google_sheets, load_to_postgresql

SPREADSHEET_ID = "19_eDQI2k5Aw0Ji5ammIlADVCYCuIpgSfVL9vtbYrlpY"
DB_CONNECTION = "postgresql://postgres.zaadqvjcvajukqelendk:sumireispurpletrash@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

def main():
    print("=== MULAI ETL PIPELINE ===")

    print("\n[1] Extracting...")
    raw_data = scrape_all()

    print("\n[2] Transforming...")
    df = transform(raw_data)

    print("\n[3] Loading...")
    load_to_csv(df, "products.csv")
    load_to_google_sheets(df, SPREADSHEET_ID, "google-sheets-api.json")
    load_to_postgresql(df, DB_CONNECTION)

    print("\n=== ETL SELESAI ===")

if __name__ == "__main__":
    main()