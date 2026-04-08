# HRDQso: Read-Only MySQL Model

## Overview

The `HRDQso` model provides read-only access to a remote Ham Radio Deluxe (HRD) QSO (contact) log database running on a separate MySQL instance. This model allows MJlog to query historical QSO records without modifying them.

## Connection Details

- **Host**: 192.168.1.177
- **Port**: 3306 (default MySQL)
- **Username**: hrd
- **Password**: hrd
- **Database**: hrd
- **Table**: table_hrd_contacts_v07
- **Records**: 20,796+ QSOs

## Model Structure

The `HRDQso` model is defined in `src/mjlog/db/models.py` and maps to the remote MySQL table with the following column categories:

### Primary Key
- `col_primary_key` (BIGINT, auto-increment)

### Core QSO Data
- `col_qso_date` (Date) - QSO date
- `col_time_on` (Time) - Start time
- `col_time_off` (Time) - End time
- `col_call` (String) - Contacted station callsign
- `col_freq` (Integer) - Frequency in Hz
- `col_freq_rx` (Integer) - Receive frequency in Hz
- `col_mode` (String) - Transmission mode (CW, SSB, etc.)
- `col_submode` (String) - Mode variant (e.g., USB, LSB, USB-D)
- `col_rst_sent` (String) - Signal report sent
- `col_rst_rcvd` (String) - Signal report received
- `col_tx_pwr` (Float) - Transmit power in watts
- `col_rx_pwr` (Float) - Receive power level

### Location Data
- `col_lat` / `col_lon` (Float) - Contacted station coordinates
- `col_my_lat` / `col_my_lon` (Float) - Own station coordinates
- `col_gridsquare` (String) - Grid square of contacted station
- `col_my_gridsquare` (String) - Own grid square
- `col_qth` (String) - QTH (location) description
- `col_my_city` (String) - Own city
- `col_my_state` (String) - Own state/province
- `col_state` (String) - Contacted station state/province

### DXCC/Zone Data
- `col_dxcc` (String) - DXCC entity code
- `col_my_dxcc` (String) - Own DXCC entity code
- `col_country` (String) - Country name
- `col_my_country` (String) - Own country name
- `col_cqz` (Integer) - CQ Zone
- `col_my_cq_zone` (Integer) - Own CQ Zone
- `col_ituz` (Integer) - ITU Zone
- `col_my_itu_zone` (Integer) - Own ITU Zone
- `col_cont` (String) - Continent code

### Station Identifiers
- `col_station_callsign` (String) - Own station callsign used
- `col_operator` (String) - Operator name
- `col_contacted_op` (String) - Contacted operator name
- `col_name` (String) - Contacted station name/operator

### QSL Tracking
- `col_qsl_sent` / `col_qsl_rcvd` (String) - Direct QSL status (Y/N/R/I)
- `col_qsl_sent_via` / `col_qsl_rcvd_via` (String) - QSL method (B=Bureau, D=Direct, E=eQSL, L=LoTW)
- `col_qslsdate` / `col_qslrdate` (Date) - QSL sent/received dates

### LoTW (Logbook of the World) Tracking
- `col_lotw_qsl_sent` / `col_lotw_qsl_rcvd` (String) - LoTW confirmation status
- `col_lotw_qslsdate` / `col_lotw_qslrdate` (Date) - LoTW dates

### eQSL Tracking
- `col_eqsl_qsl_sent` / `col_eqsl_qsl_rcvd` (String) - eQSL confirmation status
- `col_eqsl_qslsdate` / `col_eqsl_qslrdate` (Date) - eQSL dates

### Contest Data
- `col_contest_id` (String) - Contest identifier
- `col_stx` (Integer) - Serial number transmitted
- `col_stx_string` (String) - Exchange sent
- `col_srx` (Integer) - Serial number received
- `col_srx_string` (String) - Exchange received
- `col_check` (String) - Contest check
- `col_precedence` (String) - Message precedence

### Special Awards
- `col_iota` (String) - Island on the Air reference
- `col_iota_island_id` (Integer) - IOTA island ID
- `col_my_iota` (String) - Own IOTA reference
- `col_sota_ref` (String) - Summits on the Air reference
- `col_my_sota_ref` (String) - Own SOTA reference
- `col_wwff_ref` (String) - World Wide Flora & Fauna reference
- `col_my_wwff_ref` (String) - Own WWFF reference
- `col_pota_ref` (String) - Parks on the Air reference
- `col_my_pota_ref` (String) - Own POTA reference
- `col_usaca_counties` (String) - USACA county references

### Notes & Comments
- `col_comment` (String) - QSO comment
- `col_notes` (String) - Additional notes

### Propagation Data
- `col_prop_mode` (String) - Propagation mode (Es, F2, Tr, etc.)
- `col_sfi` (Integer) - Solar Flux Index
- `col_k_index` (Integer) - K-index (geomagnetic)
- `col_a_index` (Float) - A-index (geomagnetic)
- `col_max_bursts` (Integer) - Maximum meteor scatter bursts
- `col_nr_bursts` (Integer) - Number of bursts
- `col_nr_pings` (Integer) - Number of pings (EME/scatter)
- `col_ms_shower` (String) - Meteor shower name

### Equipment
- `col_rig` (String) - Contacted station rig
- `col_my_rig` (String) - Own transceiver
- `col_ant_az` (Float) - Antenna azimuth
- `col_ant_el` (Float) - Antenna elevation

## Usage Examples

### Basic Setup

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from mjlog.db.models import HRDQso

# Connect to MySQL
connection_string = "mysql+pymysql://hrd:hrd@192.168.1.177:3306/hrd"
engine = create_engine(connection_string)
```

### Query Examples

```python
from sqlalchemy import and_

session = Session(engine)

# Count total QSOs
total = session.query(HRDQso).count()

# Get all CW contacts
cw_qsos = session.query(HRDQso).filter(HRDQso.col_mode == 'CW').all()

# Get recent QSOs
recent = session.query(HRDQso).order_by(
    HRDQso.col_qso_date.desc()
).limit(100).all()

# Find QSOs with a specific country
japan_qsos = session.query(HRDQso).filter(
    HRDQso.col_country == 'Japan'
).all()

# Find all LoTW confirmations
lotw_confirmed = session.query(HRDQso).filter(
    HRDQso.col_lotw_qsl_rcvd == 'Y'
).all()

# Count QSOs by mode
from sqlalchemy import func
mode_stats = session.query(
    HRDQso.col_mode,
    func.count(HRDQso.col_primary_key)
).group_by(HRDQso.col_mode).all()

# Find QSOs from a date range
from datetime import date
qsos = session.query(HRDQso).filter(
    and_(
        HRDQso.col_qso_date >= date(2024, 1, 1),
        HRDQso.col_qso_date < date(2024, 12, 31)
    )
).all()
```

## Important Notes

### Read-Only Access

The HRDQso model is designed for **read-only access** to the remote HRD database. While SQLAlchemy allows INSERT/UPDATE/DELETE operations, these should **not be used** as the table is considered a read-only external data source.

To enforce read-only behavior at the application level:

```python
# DO: Read queries only
qsos = session.query(HRDQso).filter(...).all()

# DON'T: Write operations
session.add(new_qso)  # Don't do this!
session.delete(qso)   # Don't do this!
```

### Connection String

The connection string uses the `mysql+pymysql://` dialect. This requires `PyMySQL` to be installed, which is listed in `pyproject.toml` dependencies.

If connecting fails:
- Verify network connectivity to 192.168.1.177:3306
- Check MySQL credentials (hrd/hrd)
- Confirm the MySQL server is running
- Check firewall rules

### Column Naming Convention

All column names in the remote table follow an ALL_CAPS naming convention (COL_CALL, COL_QSO_DATE, etc.). The Python model maps these to snake_case attributes (col_call, col_qso_date) for consistency with Python conventions.

### Indexed Columns for Performance

The following columns have database indexes for efficient querying:
- `col_qso_date` - Essential for date range queries
- `col_call` - Essential for callsign lookups
- `col_mode` - Important for mode filtering
- `col_gridsquare` - For grid square searches
- `col_dxcc` - For DXCC entity filtering
- `col_cqz` / `col_ituz` - For zone-based queries
- `col_cont` - For continent filtering
- `col_iota` - For IOTA award tracking
- `col_station_callsign` - For station identification

## Testing

The HRDQso model can be tested by querying the live MySQL database:

```bash
# Test the model imports and connects
uv run python -c "
from sqlalchemy import create_engine
from mjlog.db.models import HRDQso

engine = create_engine('mysql+pymysql://hrd:hrd@192.168.1.177:3306/hrd')
qsos = engine.execute(select(func.count(HRDQso.col_primary_key))).scalar()
print(f'Total QSOs: {qsos}')
"
```

## Integration with MJlog

### In CLI Commands

```python
from mjlog.db.models import HRDQso
from sqlalchemy.orm import Session

def export_hrd_qsos(mode=None):
    """Export QSOs from HRD database."""
    engine = create_engine("mysql+pymysql://hrd:hrd@192.168.1.177:3306/hrd")
    
    with Session(engine) as session:
        query = session.query(HRDQso)
        if mode:
            query = query.filter(HRDQso.col_mode == mode)
        
        for qso in query.all():
            print(f"{qso.col_qso_date} {qso.col_call} {qso.col_mode}")
```

### In GUI Windows

```python
from mjlog.db.models import HRDQso
from sqlalchemy.orm import Session

class HRDQsoWindow(QWidget):
    def load_qsos(self):
        """Load recent QSOs from HRD database."""
        engine = create_engine("mysql+pymysql://hrd:hrd@192.168.1.177:3306/hrd")
        
        with Session(engine) as session:
            qsos = session.query(HRDQso).order_by(
                HRDQso.col_qso_date.desc()
            ).limit(100).all()
            
            self.populate_table(qsos)
```

## Future Enhancements

- [ ] Cache frequently accessed data locally
- [ ] Add SQLAlchemy event listeners for read-only enforcement
- [ ] Create views for common query patterns (recent QSOs, by mode, by country)
- [ ] Add logging for all database access
- [ ] Implement connection pooling for better performance
- [ ] Add data synchronization to local PostgreSQL database

## Troubleshooting

### Connection Refused

```
Error: [Errno 111] Connection refused
```
- Verify MySQL is running on 192.168.1.177
- Check port 3306 is accessible
- Verify network connectivity: `ping 192.168.1.177`

### Authentication Failed

```
Error: 1045: Access denied for user 'hrd'@'192.168.1.177'
```
- Verify username and password are correct
- Check MySQL user permissions on the database

### Table Not Found

```
Error: 1146: Table 'hrd.table_hrd_contacts_v07' doesn't exist
```
- Verify table name is correct (case-sensitive on Linux)
- Ensure the MySQL database and table exist

### No Module Named 'pymysql'

```
ModuleNotFoundError: No module named 'pymysql'
```
- Run `uv sync` to install dependencies
- Verify `pymysql>=1.1.0` is in `pyproject.toml`

## References

- [SQLAlchemy Column Types](https://docs.sqlalchemy.org/en/20/core/types.html)
- [PyMySQL Documentation](https://pymysql.readthedocs.io/)
- [HAM Radio Deluxe (HRD)](https://www.ham-radio-deluxe.com/)
- [DXCC Prefixes](http://www.arrl.org/dxcc/)
