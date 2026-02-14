# SUPERNOVA
Python-based internal vulnerability scanner for lab use.

vuln-scanner/
│
├── main.py
│
├── requirements.txt
│
├── README.md
│
├── config/
│   └── settings.py
│
├── scanner/
│   ├── __init__.py
│   ├── host_discovery.py
│   ├── port_scanner.py
│   └── service_detection.py
│
├── checks/
│   ├── __init__.py
│   ├── ftp_check.py
│   ├── smb_check.py
│   ├── http_check.py
│   ├── telnet_check.py
│   └── rdp_check.py
│
├── cve/
│   ├── __init__.py
│   ├── cve_mapper.py
│   └── cve_database.json
│
├── report/
│   ├── __init__.py
│   ├── report_generator.py
│   └── templates/
│       └── report_template.html
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── helpers.py
│   └── validator.py
│
├── output/
│   ├── scan_report.json
│   └── scan_report.html
│
└── tests/
    ├── test_scanner.py
    └── test_checks.py
