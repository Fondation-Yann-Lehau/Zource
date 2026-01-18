# Zource

**International Telecommunications Union Resource Management System**

A complete and unique system for managing telecommunications resources, frequency allocations, and spectrum management in accordance with ITU standards.

## Overview

Zource is a comprehensive telecommunications resource management system designed to help manage and track frequency allocations, service types, and telecommunications resources across different countries and regions, following International Telecommunications Union (ITU) guidelines.

## Features

- ✅ **Frequency Band Management**: Support for all ITU frequency bands (VLF, LF, MF, HF, VHF, UHF, SHF, EHF)
- ✅ **Service Type Classification**: Manage different telecommunications services (Fixed, Mobile, Broadcasting, Satellite, etc.)
- ✅ **Conflict Detection**: Automatic detection of frequency allocation conflicts
- ✅ **Resource Tracking**: Complete allocation and deallocation history
- ✅ **Multi-Country Support**: Manage resources across different countries with ISO country codes
- ✅ **Import/Export**: JSON-based data persistence and exchange
- ✅ **Comprehensive Reporting**: Generate detailed allocation reports

## Installation

### Prerequisites
- Python 3.7 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Fondation-Yann-Lehau/Zource.git
cd Zource
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the System

Run the main system with example data:
```bash
python3 zource.py
```

### Basic Example

```python
from zource import ITUResourceManager, TelecomResource, FrequencyBand, ServiceType

# Create resource manager
manager = ITUResourceManager()

# Create a new telecommunications resource
resource = TelecomResource(
    resource_id="FR-VHF-001",
    frequency_band=FrequencyBand.VHF,
    service_type=ServiceType.BROADCASTING,
    country_code="FRA",
    allocated_date="2026-01-18",
    frequency_range=(88.0, 108.0),
    description="FM Radio Broadcasting"
)

# Allocate the resource
manager.allocate_resource(resource)

# List all active resources
for r in manager.list_resources():
    print(f"{r.resource_id}: {r.service_type.value}")

# Generate a report
print(manager.generate_report())

# Export to JSON
manager.export_to_json("resources.json")
```

## Frequency Bands

The system supports all ITU frequency band classifications:

| Band | Name | Frequency Range |
|------|------|----------------|
| VLF | Very Low Frequency | 3-30 kHz |
| LF | Low Frequency | 30-300 kHz |
| MF | Medium Frequency | 300-3000 kHz |
| HF | High Frequency | 3-30 MHz |
| VHF | Very High Frequency | 30-300 MHz |
| UHF | Ultra High Frequency | 300-3000 MHz |
| SHF | Super High Frequency | 3-30 GHz |
| EHF | Extremely High Frequency | 30-300 GHz |

## Service Types

Supported ITU service type classifications:

- **Fixed Service**: Point-to-point communications
- **Mobile Service**: Mobile communications
- **Broadcasting Service**: Radio and TV broadcasting
- **Satellite Service**: Satellite communications
- **Radio Astronomy Service**: Radio astronomy observations
- **Maritime Service**: Maritime communications
- **Aeronautical Service**: Aviation communications
- **Amateur Radio Service**: Amateur radio operations

## Testing

Run the test suite:
```bash
python3 -m pytest test_zource.py -v
```

Run with coverage:
```bash
python3 -m pytest test_zource.py --cov=zource --cov-report=html
```

## API Reference

### ITUResourceManager

Main class for managing telecommunications resources.

**Methods:**
- `allocate_resource(resource: TelecomResource) -> bool`: Allocate a new resource
- `deallocate_resource(resource_id: str) -> bool`: Deallocate a resource
- `get_resource(resource_id: str) -> Optional[TelecomResource]`: Retrieve a resource by ID
- `list_resources(service_type, country_code, active_only) -> List[TelecomResource]`: List resources with filters
- `export_to_json(filename: str)`: Export all resources to JSON
- `import_from_json(filename: str)`: Import resources from JSON
- `generate_report() -> str`: Generate comprehensive allocation report

### TelecomResource

Dataclass representing a telecommunications resource allocation.

**Attributes:**
- `resource_id`: Unique identifier for the resource
- `frequency_band`: ITU frequency band classification
- `service_type`: Type of telecommunications service
- `country_code`: ISO country code
- `allocated_date`: Date of allocation
- `frequency_range`: Tuple of (start_freq, end_freq) in MHz
- `description`: Human-readable description
- `is_active`: Whether the resource is currently active

## Project Structure

```
Zource/
├── zource.py           # Main system implementation
├── test_zource.py      # Comprehensive test suite
├── requirements.txt    # Python dependencies
├── package.json        # Project metadata
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Contributing

Contributions are welcome! Please ensure:
1. All tests pass
2. Code follows PEP 8 style guidelines
3. New features include appropriate tests
4. Documentation is updated

## License

MIT License - See LICENSE file for details

## Author

Fondation Yann Lehau

## Acknowledgments

This project follows International Telecommunications Union (ITU) standards and guidelines for frequency allocation and spectrum management.
