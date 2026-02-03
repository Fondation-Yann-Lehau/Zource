#!/usr/bin/env python3
"""
Zource - International Telecommunications Union Resource Management System
A complete and unique system for managing telecommunications resources.
"""

import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class FrequencyBand(Enum):
    """ITU frequency band classifications"""
    VLF = "Very Low Frequency (3-30 kHz)"
    LF = "Low Frequency (30-300 kHz)"
    MF = "Medium Frequency (300-3000 kHz)"
    HF = "High Frequency (3-30 MHz)"
    VHF = "Very High Frequency (30-300 MHz)"
    UHF = "Ultra High Frequency (300-3000 MHz)"
    SHF = "Super High Frequency (3-30 GHz)"
    EHF = "Extremely High Frequency (30-300 GHz)"


class ServiceType(Enum):
    """ITU service type classifications"""
    FIXED = "Fixed Service"
    MOBILE = "Mobile Service"
    BROADCASTING = "Broadcasting Service"
    SATELLITE = "Satellite Service"
    RADIO_ASTRONOMY = "Radio Astronomy Service"
    MARITIME = "Maritime Service"
    AERONAUTICAL = "Aeronautical Service"
    AMATEUR = "Amateur Radio Service"


@dataclass
class TelecomResource:
    """Represents a telecommunications resource allocation"""
    resource_id: str
    frequency_band: FrequencyBand
    service_type: ServiceType
    country_code: str
    allocated_date: str
    frequency_range: tuple
    description: str
    is_active: bool = True

    def to_dict(self) -> dict:
        """Convert resource to dictionary"""
        data = asdict(self)
        data['frequency_band'] = self.frequency_band.name
        data['service_type'] = self.service_type.name
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'TelecomResource':
        """Create resource from dictionary"""
        data['frequency_band'] = FrequencyBand[data['frequency_band']]
        data['service_type'] = ServiceType[data['service_type']]
        return cls(**data)


class ITUResourceManager:
    """Main resource management system for ITU telecommunications"""
    
    def __init__(self):
        self.resources: Dict[str, TelecomResource] = {}
        self.allocation_history: List[Dict] = []
    
    def allocate_resource(self, resource: TelecomResource) -> bool:
        """Allocate a new telecommunications resource"""
        if resource.resource_id in self.resources:
            print(f"Error: Resource {resource.resource_id} already exists")
            return False
        
        # Check for frequency conflicts
        if self._check_frequency_conflict(resource):
            print(f"Error: Frequency conflict detected for {resource.resource_id}")
            return False
        
        self.resources[resource.resource_id] = resource
        self._log_allocation(resource, "ALLOCATED")
        print(f"Successfully allocated resource: {resource.resource_id}")
        return True
    
    def deallocate_resource(self, resource_id: str) -> bool:
        """Deallocate a telecommunications resource"""
        if resource_id not in self.resources:
            print(f"Error: Resource {resource_id} not found")
            return False
        
        resource = self.resources[resource_id]
        resource.is_active = False
        self._log_allocation(resource, "DEALLOCATED")
        print(f"Successfully deallocated resource: {resource_id}")
        return True
    
    def get_resource(self, resource_id: str) -> Optional[TelecomResource]:
        """Retrieve a resource by ID"""
        return self.resources.get(resource_id)
    
    def list_resources(self, service_type: Optional[ServiceType] = None,
                      country_code: Optional[str] = None,
                      active_only: bool = True) -> List[TelecomResource]:
        """List resources with optional filtering"""
        filtered = []
        for resource in self.resources.values():
            if active_only and not resource.is_active:
                continue
            if service_type and resource.service_type != service_type:
                continue
            if country_code and resource.country_code != country_code:
                continue
            filtered.append(resource)
        return filtered
    
    def _check_frequency_conflict(self, new_resource: TelecomResource) -> bool:
        """Check if frequency range conflicts with existing allocations"""
        new_start, new_end = new_resource.frequency_range
        
        for resource in self.resources.values():
            if not resource.is_active:
                continue
            if resource.country_code != new_resource.country_code:
                continue
            
            existing_start, existing_end = resource.frequency_range
            
            # Check for overlap
            if (new_start <= existing_end and new_end >= existing_start):
                return True
        
        return False
    
    def _log_allocation(self, resource: TelecomResource, action: str):
        """Log resource allocation/deallocation"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'resource_id': resource.resource_id,
            'country_code': resource.country_code,
            'service_type': resource.service_type.name
        }
        self.allocation_history.append(log_entry)
    
    def export_to_json(self, filename: str):
        """Export all resources to JSON file"""
        data = {
            'resources': [r.to_dict() for r in self.resources.values()],
            'history': self.allocation_history
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Exported data to {filename}")
    
    def import_from_json(self, filename: str):
        """Import resources from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        for resource_data in data.get('resources', []):
            resource = TelecomResource.from_dict(resource_data)
            self.resources[resource.resource_id] = resource
        
        self.allocation_history.extend(data.get('history', []))
        print(f"Imported {len(data.get('resources', []))} resources from {filename}")
    
    def generate_report(self) -> str:
        """Generate a comprehensive resource allocation report"""
        report = []
        report.append("=" * 80)
        report.append("ITU TELECOMMUNICATIONS RESOURCE ALLOCATION REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Resources: {len(self.resources)}")
        report.append(f"Active Resources: {len([r for r in self.resources.values() if r.is_active])}")
        report.append("")
        
        # Group by country
        by_country = {}
        for resource in self.resources.values():
            if resource.is_active:
                by_country.setdefault(resource.country_code, []).append(resource)
        
        report.append("RESOURCES BY COUNTRY:")
        report.append("-" * 80)
        for country, resources in sorted(by_country.items()):
            report.append(f"\n{country}: {len(resources)} allocations")
            for resource in resources:
                freq_start, freq_end = resource.frequency_range
                report.append(f"  - {resource.resource_id}: {resource.service_type.value}")
                report.append(f"    Frequency: {freq_start}-{freq_end} MHz")
                report.append(f"    Band: {resource.frequency_band.value}")
        
        report.append("\n" + "=" * 80)
        return "\n".join(report)


def main():
    """Main demonstration of the ITU Resource Management System"""
    print("Zource - ITU Telecommunications Resource Management System")
    print("=" * 60)
    
    # Create manager
    manager = ITUResourceManager()
    
    # Example allocations
    resources = [
        TelecomResource(
            resource_id="FR-VHF-001",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.BROADCASTING,
            country_code="FRA",
            allocated_date="2026-01-18",
            frequency_range=(88.0, 108.0),
            description="FM Radio Broadcasting"
        ),
        TelecomResource(
            resource_id="FR-UHF-001",
            frequency_band=FrequencyBand.UHF,
            service_type=ServiceType.MOBILE,
            country_code="FRA",
            allocated_date="2026-01-18",
            frequency_range=(880.0, 915.0),
            description="Mobile Communications"
        ),
        TelecomResource(
            resource_id="UK-VHF-001",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.AERONAUTICAL,
            country_code="GBR",
            allocated_date="2026-01-18",
            frequency_range=(118.0, 137.0),
            description="Aeronautical Communications"
        ),
    ]
    
    # Allocate resources
    print("\nAllocating resources...")
    for resource in resources:
        manager.allocate_resource(resource)
    
    # List resources
    print("\nListing active resources:")
    for resource in manager.list_resources():
        print(f"  {resource.resource_id}: {resource.service_type.value}")
    
    # Generate report
    print("\n" + manager.generate_report())
    
    # Export data
    print("\nExporting data...")
    manager.export_to_json("itu_resources.json")


if __name__ == "__main__":
    main()
