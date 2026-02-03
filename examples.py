#!/usr/bin/env python3
"""
Example usage scenarios for the Zource ITU Resource Management System
"""

from zource import (
    ITUResourceManager, TelecomResource, FrequencyBand, ServiceType
)


def example_basic_allocation():
    """Example: Basic resource allocation"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Resource Allocation")
    print("="*70)
    
    manager = ITUResourceManager()
    
    # Allocate a VHF mobile service
    mobile_resource = TelecomResource(
        resource_id="USA-VHF-MOB-001",
        frequency_band=FrequencyBand.VHF,
        service_type=ServiceType.MOBILE,
        country_code="USA",
        allocated_date="2026-01-18",
        frequency_range=(150.0, 174.0),
        description="Public Safety and Business Mobile Radio"
    )
    
    manager.allocate_resource(mobile_resource)
    print("\nResource allocated successfully!")


def example_conflict_detection():
    """Example: Frequency conflict detection"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Frequency Conflict Detection")
    print("="*70)
    
    manager = ITUResourceManager()
    
    # First allocation
    resource1 = TelecomResource(
        resource_id="FRA-FM-001",
        frequency_band=FrequencyBand.VHF,
        service_type=ServiceType.BROADCASTING,
        country_code="FRA",
        allocated_date="2026-01-18",
        frequency_range=(88.0, 100.0),
        description="FM Radio - Paris Region"
    )
    manager.allocate_resource(resource1)
    
    # Attempt conflicting allocation
    resource2 = TelecomResource(
        resource_id="FRA-FM-002",
        frequency_band=FrequencyBand.VHF,
        service_type=ServiceType.BROADCASTING,
        country_code="FRA",
        allocated_date="2026-01-18",
        frequency_range=(95.0, 105.0),  # Overlaps with resource1
        description="FM Radio - Lyon Region"
    )
    
    print("\nAttempting to allocate overlapping frequency...")
    result = manager.allocate_resource(resource2)
    
    if not result:
        print("✓ Conflict detected and prevented!")


def example_multi_country_management():
    """Example: Managing resources across multiple countries"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Multi-Country Resource Management")
    print("="*70)
    
    manager = ITUResourceManager()
    
    # Allocate resources for different countries
    countries = [
        ("FRA", "France - Aviation Communications"),
        ("DEU", "Germany - Aviation Communications"),
        ("GBR", "UK - Aviation Communications"),
    ]
    
    for idx, (country, description) in enumerate(countries, 1):
        resource = TelecomResource(
            resource_id=f"{country}-AER-00{idx}",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.AERONAUTICAL,
            country_code=country,
            allocated_date="2026-01-18",
            frequency_range=(118.0, 137.0),
            description=description
        )
        manager.allocate_resource(resource)
    
    # List resources by country
    print("\nResources for France:")
    france_resources = manager.list_resources(country_code="FRA")
    for r in france_resources:
        print(f"  {r.resource_id}: {r.description}")
    
    print("\nResources for Germany:")
    germany_resources = manager.list_resources(country_code="DEU")
    for r in germany_resources:
        print(f"  {r.resource_id}: {r.description}")


def example_service_filtering():
    """Example: Filtering resources by service type"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Service Type Filtering")
    print("="*70)
    
    manager = ITUResourceManager()
    
    # Allocate different service types
    services = [
        (ServiceType.MOBILE, "Mobile Communications", (450.0, 470.0)),
        (ServiceType.BROADCASTING, "FM Radio", (88.0, 108.0)),
        (ServiceType.SATELLITE, "Satellite Downlink", (11700.0, 12200.0)),
        (ServiceType.AMATEUR, "Amateur Radio", (144.0, 148.0)),
    ]
    
    for idx, (service_type, description, freq_range) in enumerate(services, 1):
        resource = TelecomResource(
            resource_id=f"INT-{service_type.name}-00{idx}",
            frequency_band=FrequencyBand.VHF if freq_range[0] < 300 else FrequencyBand.SHF,
            service_type=service_type,
            country_code="INT",
            allocated_date="2026-01-18",
            frequency_range=freq_range,
            description=description
        )
        manager.allocate_resource(resource)
    
    # Filter by service type
    print("\nMobile Services:")
    mobile_services = manager.list_resources(service_type=ServiceType.MOBILE)
    for r in mobile_services:
        print(f"  {r.resource_id}: {r.description}")
    
    print("\nBroadcasting Services:")
    broadcast_services = manager.list_resources(service_type=ServiceType.BROADCASTING)
    for r in broadcast_services:
        print(f"  {r.resource_id}: {r.description}")


def example_import_export():
    """Example: Import and export functionality"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Import/Export Functionality")
    print("="*70)
    
    # Create and populate manager
    manager1 = ITUResourceManager()
    
    resource = TelecomResource(
        resource_id="EXPORT-TEST-001",
        frequency_band=FrequencyBand.UHF,
        service_type=ServiceType.MOBILE,
        country_code="TST",
        allocated_date="2026-01-18",
        frequency_range=(800.0, 900.0),
        description="Test Export Resource"
    )
    manager1.allocate_resource(resource)
    
    # Export
    export_file = "example_export.json"
    manager1.export_to_json(export_file)
    print(f"\nData exported to {export_file}")
    
    # Import into new manager
    manager2 = ITUResourceManager()
    manager2.import_from_json(export_file)
    print(f"Data imported from {export_file}")
    
    # Verify
    imported = manager2.get_resource("EXPORT-TEST-001")
    if imported:
        print(f"\n✓ Successfully imported: {imported.resource_id}")


def example_lifecycle_management():
    """Example: Complete resource lifecycle"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Resource Lifecycle Management")
    print("="*70)
    
    manager = ITUResourceManager()
    
    # Allocate
    resource = TelecomResource(
        resource_id="LIFECYCLE-001",
        frequency_band=FrequencyBand.VHF,
        service_type=ServiceType.MARITIME,
        country_code="INT",
        allocated_date="2026-01-18",
        frequency_range=(156.0, 162.0),
        description="International Maritime VHF"
    )
    
    print("\n1. Allocating resource...")
    manager.allocate_resource(resource)
    
    # Query
    print("\n2. Querying resource...")
    retrieved = manager.get_resource("LIFECYCLE-001")
    print(f"   Status: {'Active' if retrieved.is_active else 'Inactive'}")
    
    # Deallocate
    print("\n3. Deallocating resource...")
    manager.deallocate_resource("LIFECYCLE-001")
    
    # Verify deallocation
    retrieved = manager.get_resource("LIFECYCLE-001")
    print(f"   Status: {'Active' if retrieved.is_active else 'Inactive'}")
    
    print("\n✓ Lifecycle complete!")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("ZOURCE ITU RESOURCE MANAGEMENT SYSTEM - EXAMPLES")
    print("="*70)
    
    example_basic_allocation()
    example_conflict_detection()
    example_multi_country_management()
    example_service_filtering()
    example_import_export()
    example_lifecycle_management()
    
    print("\n" + "="*70)
    print("All examples completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
