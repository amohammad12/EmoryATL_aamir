"""
Test MongoDB Atlas connection with detailed diagnostics
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

async def test_atlas_connection():
    print("🔍 MONGODB ATLAS CONNECTION TEST")
    print("=" * 60)

    # Display configuration (hiding password)
    url = settings.MONGODB_URL
    if '@' in url:
        parts = url.split('@')
        username_part = parts[0].split('//')[1].split(':')[0]
        cluster_part = parts[1]
        masked_url = f"mongodb+srv://{username_part}:***@{cluster_part}"
    else:
        masked_url = url

    print(f"\n📍 Connection String: {masked_url}")
    print(f"📍 Database Name: {settings.MONGODB_DB_NAME}")
    print()

    try:
        # Create client
        print("1️⃣ Creating MongoDB client...")
        client = AsyncIOMotorClient(settings.MONGODB_URL)
        print("   ✅ Client created")

        # Test connection with ping
        print("\n2️⃣ Testing connection with ping...")
        await client.admin.command('ping')
        print("   ✅ Connection successful!")

        # Get server info
        print("\n3️⃣ Getting server information...")
        server_info = await client.server_info()
        print(f"   ✅ MongoDB Version: {server_info.get('version')}")

        # List databases
        print("\n4️⃣ Listing databases...")
        db_list = await client.list_database_names()
        print(f"   ✅ Available databases: {db_list}")

        # Access our database
        print(f"\n5️⃣ Accessing database '{settings.MONGODB_DB_NAME}'...")
        db = client[settings.MONGODB_DB_NAME]
        print("   ✅ Database accessed")

        # List collections
        print("\n6️⃣ Listing collections...")
        collections = await db.list_collection_names()
        if collections:
            print(f"   ✅ Existing collections: {collections}")
        else:
            print("   ⚠️  No collections yet (will be created when first song is generated)")

        # Test write operation
        print("\n7️⃣ Testing write permission...")
        test_collection = db.connection_test
        result = await test_collection.insert_one({
            "test": "MongoDB Atlas connection successful!",
            "timestamp": "2025-11-15"
        })
        print(f"   ✅ Write successful! Document ID: {result.inserted_id}")

        # Test read operation
        print("\n8️⃣ Testing read permission...")
        doc = await test_collection.find_one({"_id": result.inserted_id})
        print(f"   ✅ Read successful! Document: {doc['test']}")

        # Clean up test data
        print("\n9️⃣ Cleaning up test data...")
        await test_collection.delete_one({"_id": result.inserted_id})
        print("   ✅ Test data cleaned")

        # Summary
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("✅ MongoDB Atlas is properly configured")
        print("✅ Read/Write permissions working")
        print("✅ Ready for pirate karaoke app!")
        print()
        print("📊 Configuration Summary:")
        print(f"   • Cluster: {cluster_part}")
        print(f"   • Database: {settings.MONGODB_DB_NAME}")
        print(f"   • Collections: Will be auto-created (jobs, song_cache)")

        client.close()
        return True

    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ CONNECTION FAILED!")
        print("=" * 60)
        print(f"\nError: {str(e)}")
        print()
        print("🔍 Troubleshooting:")
        print("   1. Check username/password in .env file")
        print("   2. Verify network access allows 0.0.0.0/0 in Atlas")
        print("   3. Ensure cluster is active (not paused)")
        print("   4. Check database user exists with correct privileges")
        print()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_atlas_connection())
    exit(0 if success else 1)
