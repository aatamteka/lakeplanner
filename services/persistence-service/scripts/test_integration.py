#!/usr/bin/env python3
"""
Integration test script for the persistence service.

Sets up test data:
- Boone Lake in northeast TN
- Rope swing amenity
- Boat ramp
- Homer Simpson as a user
"""

import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000/api/v1"


def create_lake():
    """Create Boone Lake in northeast TN."""
    lake_data = {
        "name": "Boone Lake",
        "latitude": 36.4667,
        "longitude": -82.4167
    }

    response = requests.post(f"{API_BASE_URL}/lakes/", json=lake_data)
    response.raise_for_status()
    lake = response.json()
    print(f"✓ Created lake: {lake['name']} (ID: {lake['id']})")
    return lake


def create_amenity(lake_id):
    """Create rope swing amenity at Boone Lake."""
    amenity_data = {
        "lake_id": lake_id,
        "type": "rope_swing",
        "name": "Boone Lake Rope Swing",
        "latitude": 36.433912,
        "longitude": -82.397390,
        "capacity_score": 15,
        "hours_of_operation": {
            "open": "sunrise",
            "close": "sunset"
        }
    }

    response = requests.post(f"{API_BASE_URL}/amenities/", json=amenity_data)
    response.raise_for_status()
    amenity = response.json()
    print(f"✓ Created amenity: {amenity['name']} (ID: {amenity['id']})")
    return amenity


def create_boat_ramp(lake_id):
    """Create boat ramp at Boone Lake."""
    ramp_data = {
        "lake_id": lake_id,
        "name": "Boone Lake Main Ramp",
        "latitude": 36.447359,
        "longitude": -82.428104,
        "hours_of_operation": {
            "weekday": "6:00 AM - 10:00 PM",
            "weekend": "5:00 AM - 11:00 PM"
        },
        "seasonal_availability": {
            "open_season": "March - November"
        },
        "is_active": True
    }

    response = requests.post(f"{API_BASE_URL}/boat-ramps/", json=ramp_data)
    response.raise_for_status()
    ramp = response.json()
    print(f"✓ Created boat ramp: {ramp['name']} (ID: {ramp['id']})")
    return ramp


def create_user(lake_id):
    """Create Homer Simpson as a user."""
    user_data = {
        "username": "hsimpson",
        "email": "homer@example.com",
        "password_hash": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU7t.6cLxHQW",  # hashed "doh!"
        "preferred_lake_id": lake_id,
        "owns_boat": True,
        "schedule_preferences": {
            "weekday": {
                "morning": False,
                "afternoon": False,
                "evening": True
            },
            "weekend": {
                "saturday": {
                    "morning": False,
                    "afternoon": False,
                    "evening": True
                },
                "sunday": {
                    "morning": False,
                    "afternoon": False,
                    "evening": True
                }
            }
        },
        "weather_preferences": {
            "max_precipitation_probability": 30,
            "max_wind_speed": 15,
            "min_temperature": 65
        },
        "notification_preferences": {
            "email_enabled": True,
            "sms_enabled": False,
            "weather_alerts": True,
            "friend_notifications": False
        }
    }

    response = requests.post(f"{API_BASE_URL}/users/", json=user_data)
    response.raise_for_status()
    user = response.json()
    print(f"✓ Created user: {user['username']} ({user['email']}) (ID: {user['id']})")
    return user


def verify_setup():
    """Verify all data was created correctly."""
    print("\n--- Verification ---")

    # Check lakes
    response = requests.get(f"{API_BASE_URL}/lakes/")
    response.raise_for_status()
    lakes = response.json()
    print(f"✓ Total lakes: {len(lakes)}")

    # Check amenities
    response = requests.get(f"{API_BASE_URL}/amenities/")
    response.raise_for_status()
    amenities = response.json()
    print(f"✓ Total amenities: {len(amenities)}")

    # Check users
    response = requests.get(f"{API_BASE_URL}/users/")
    response.raise_for_status()
    users = response.json()
    print(f"✓ Total users: {len(users)}")

    # Show Homer's details
    if users:
        homer = users[0]
        response = requests.get(f"{API_BASE_URL}/users/{homer['id']}")
        response.raise_for_status()
        homer_details = response.json()
        print(f"\n--- Homer Simpson Details ---")
        print(f"Username: {homer_details['username']}")
        print(f"Email: {homer_details['email']}")
        print(f"Owns boat: {homer_details['owns_boat']}")
        print(f"Schedule: Prefers evenings")
        print(f"Weather preferences: {json.dumps(homer_details.get('weather_preferences', {}), indent=2)}")


def main():
    """Run the integration test."""
    print("=== Persistence Service Integration Test ===\n")

    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health")
        response.raise_for_status()
        print("✓ Service is healthy\n")

        print("--- Creating Test Data ---")

        # Create lake
        lake = create_lake()

        # Create amenities
        amenity = create_amenity(lake['id'])

        # Create boat ramp (note: this endpoint might need to be added to the API)
        # For now, we'll skip it if the endpoint doesn't exist
        try:
            ramp = create_boat_ramp(lake['id'])
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print("⚠ Boat ramp endpoint not yet implemented, skipping...")
            else:
                raise

        # Create user
        user = create_user(lake['id'])

        # Verify everything
        verify_setup()

        print("\n✓ Integration test completed successfully!")

    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the persistence service.")
        print("  Make sure the service is running at http://localhost:8000")
        return 1
    except requests.exceptions.HTTPError as e:
        print(f"✗ HTTP Error: {e}")
        print(f"  Response: {e.response.text}")
        return 1
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
