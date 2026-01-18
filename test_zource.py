"""
Unit tests for the Zource ITU Resource Management System
"""

import pytest
import json
import os
from zource import (
    ITUResourceManager, TelecomResource, FrequencyBand, 
    ServiceType
)


class TestTelecomResource:
    """Test TelecomResource dataclass functionality"""
    
    def test_resource_creation(self):
        """Test creating a telecommunications resource"""
        resource = TelecomResource(
            resource_id="TEST-001",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.MOBILE,
            country_code="TST",
            allocated_date="2026-01-18",
            frequency_range=(100.0, 200.0),
            description="Test resource"
        )
        assert resource.resource_id == "TEST-001"
        assert resource.is_active is True
        assert resource.frequency_band == FrequencyBand.VHF
    
    def test_resource_to_dict(self):
        """Test converting resource to dictionary"""
        resource = TelecomResource(
            resource_id="TEST-001",
            frequency_band=FrequencyBand.UHF,
            service_type=ServiceType.BROADCASTING,
            country_code="TST",
            allocated_date="2026-01-18",
            frequency_range=(500.0, 600.0),
            description="Test resource"
        )
        data = resource.to_dict()
        assert data['resource_id'] == "TEST-001"
        assert data['frequency_band'] == "UHF"
        assert data['service_type'] == "BROADCASTING"
    
    def test_resource_from_dict(self):
        """Test creating resource from dictionary"""
        data = {
            'resource_id': 'TEST-002',
            'frequency_band': 'VHF',
            'service_type': 'MOBILE',
            'country_code': 'TST',
            'allocated_date': '2026-01-18',
            'frequency_range': (100.0, 200.0),
            'description': 'Test',
            'is_active': True
        }
        resource = TelecomResource.from_dict(data)
        assert resource.resource_id == "TEST-002"
        assert resource.frequency_band == FrequencyBand.VHF


class TestITUResourceManager:
    """Test ITUResourceManager functionality"""
    
    @pytest.fixture
    def manager(self):
        """Create a fresh manager for each test"""
        return ITUResourceManager()
    
    @pytest.fixture
    def sample_resource(self):
        """Create a sample resource for testing"""
        return TelecomResource(
            resource_id="TEST-VHF-001",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.MOBILE,
            country_code="TST",
            allocated_date="2026-01-18",
            frequency_range=(100.0, 150.0),
            description="Test VHF resource"
        )
    
    def test_allocate_resource(self, manager, sample_resource):
        """Test allocating a new resource"""
        result = manager.allocate_resource(sample_resource)
        assert result is True
        assert sample_resource.resource_id in manager.resources
        assert len(manager.allocation_history) == 1
    
    def test_allocate_duplicate_resource(self, manager, sample_resource):
        """Test allocating duplicate resource fails"""
        manager.allocate_resource(sample_resource)
        result = manager.allocate_resource(sample_resource)
        assert result is False
    
    def test_frequency_conflict_detection(self, manager):
        """Test frequency conflict detection"""
        resource1 = TelecomResource(
            resource_id="TEST-001",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.MOBILE,
            country_code="TST",
            allocated_date="2026-01-18",
            frequency_range=(100.0, 150.0),
            description="First resource"
        )
        resource2 = TelecomResource(
            resource_id="TEST-002",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.MOBILE,
            country_code="TST",
            allocated_date="2026-01-18",
            frequency_range=(140.0, 180.0),  # Overlaps with resource1
            description="Conflicting resource"
        )
        
        assert manager.allocate_resource(resource1) is True
        assert manager.allocate_resource(resource2) is False
    
    def test_deallocate_resource(self, manager, sample_resource):
        """Test deallocating a resource"""
        manager.allocate_resource(sample_resource)
        result = manager.deallocate_resource(sample_resource.resource_id)
        assert result is True
        assert manager.resources[sample_resource.resource_id].is_active is False
    
    def test_get_resource(self, manager, sample_resource):
        """Test retrieving a resource"""
        manager.allocate_resource(sample_resource)
        retrieved = manager.get_resource(sample_resource.resource_id)
        assert retrieved is not None
        assert retrieved.resource_id == sample_resource.resource_id
    
    def test_list_resources_filter_by_country(self, manager):
        """Test listing resources filtered by country"""
        resource1 = TelecomResource(
            resource_id="FR-001",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.MOBILE,
            country_code="FRA",
            allocated_date="2026-01-18",
            frequency_range=(100.0, 150.0),
            description="France resource"
        )
        resource2 = TelecomResource(
            resource_id="UK-001",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.MOBILE,
            country_code="GBR",
            allocated_date="2026-01-18",
            frequency_range=(100.0, 150.0),
            description="UK resource"
        )
        
        manager.allocate_resource(resource1)
        manager.allocate_resource(resource2)
        
        france_resources = manager.list_resources(country_code="FRA")
        assert len(france_resources) == 1
        assert france_resources[0].country_code == "FRA"
    
    def test_list_resources_filter_by_service(self, manager):
        """Test listing resources filtered by service type"""
        resource1 = TelecomResource(
            resource_id="MOB-001",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.MOBILE,
            country_code="TST",
            allocated_date="2026-01-18",
            frequency_range=(100.0, 150.0),
            description="Mobile resource"
        )
        resource2 = TelecomResource(
            resource_id="BRD-001",
            frequency_band=FrequencyBand.VHF,
            service_type=ServiceType.BROADCASTING,
            country_code="TST",
            allocated_date="2026-01-18",
            frequency_range=(200.0, 250.0),
            description="Broadcasting resource"
        )
        
        manager.allocate_resource(resource1)
        manager.allocate_resource(resource2)
        
        mobile_resources = manager.list_resources(service_type=ServiceType.MOBILE)
        assert len(mobile_resources) == 1
        assert mobile_resources[0].service_type == ServiceType.MOBILE
    
    def test_export_import_json(self, manager, sample_resource, tmp_path):
        """Test exporting and importing data"""
        manager.allocate_resource(sample_resource)
        
        # Export
        export_file = tmp_path / "test_export.json"
        manager.export_to_json(str(export_file))
        assert os.path.exists(export_file)
        
        # Import into new manager
        new_manager = ITUResourceManager()
        new_manager.import_from_json(str(export_file))
        assert len(new_manager.resources) == 1
        assert sample_resource.resource_id in new_manager.resources
    
    def test_generate_report(self, manager, sample_resource):
        """Test generating a report"""
        manager.allocate_resource(sample_resource)
        report = manager.generate_report()
        assert "ITU TELECOMMUNICATIONS RESOURCE ALLOCATION REPORT" in report
        assert "Total Resources: 1" in report
        assert sample_resource.resource_id in report


class TestFrequencyBands:
    """Test frequency band enumeration"""
    
    def test_all_bands_exist(self):
        """Test that all ITU frequency bands are defined"""
        expected_bands = ['VLF', 'LF', 'MF', 'HF', 'VHF', 'UHF', 'SHF', 'EHF']
        for band_name in expected_bands:
            assert hasattr(FrequencyBand, band_name)
    
    def test_band_values(self):
        """Test frequency band value strings"""
        assert "Very Low Frequency" in FrequencyBand.VLF.value
        assert "Ultra High Frequency" in FrequencyBand.UHF.value


class TestServiceTypes:
    """Test service type enumeration"""
    
    def test_all_services_exist(self):
        """Test that common ITU service types are defined"""
        expected_services = ['FIXED', 'MOBILE', 'BROADCASTING', 'SATELLITE']
        for service_name in expected_services:
            assert hasattr(ServiceType, service_name)
    
    def test_service_values(self):
        """Test service type value strings"""
        assert ServiceType.MOBILE.value == "Mobile Service"
        assert ServiceType.BROADCASTING.value == "Broadcasting Service"
