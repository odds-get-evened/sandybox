import asyncio
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from geoquery import geode
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from jinja2_time import TimeExtension

app = FastAPI()
static_p = Path(Path(__file__).parent.parent.parent.parent, 'resources', 'static')
app.mount("/static", StaticFiles(directory=static_p), name='static')
template_p = Path(static_p.parent, 'templates')
templates = Jinja2Templates(directory=template_p)


@app.get("/")
def endpoint_root(req: Request):
    return templates.TemplateResponse(request=req, name="home.html")


@app.get("/items/{id}", response_class=HTMLResponse)
async def endpoint_item(request: Request, id: str):
    return templates.TemplateResponse(request=request, name="item.html", context={'id': id})


@app.get("/wx/report/{q}", response_class=HTMLResponse)
async def endpoint_wx_report(req: Request, q: str):
    data = await wx_run(q.strip())
    return templates.TemplateResponse(request=req, name="wx_report.html", context={'forecast': data[1], 'q': q.strip()})


async def async_get_lat_lng(loc: str):
    return geode.get_lat_long(loc)


async def async_get_grid(lat, lng):
    return geode.get_grid(lat, lng)


async def async_get_stations(grid):
    return geode.get_stations(grid)


async def async_get_observation(stn):
    return geode.get_observation(stn)


def iso_to_epoch(s: str):
    dt = datetime.fromisoformat(s.strip())
    return dt.timestamp()


def get_nested_values(dict_obj: dict, keys: list[str], default=None):
    """ safely get nested dictionary values """
    cur = dict_obj
    for key in keys:
        if isinstance(cur, dict):
            cur = cur.get(key, default)
        else:
            return default

    return cur


def deep_dict_merge(d1: dict, d2: dict):
    """ merge 2 dictionaries recursively """
    res = d1.copy()

    for key, val in d2.items():
        if key in res and isinstance(res[key], dict) and isinstance(val, dict):
            res[key] = deep_dict_merge(res[key], val)
        else:
            res[key] = val

    return res


def forecast_to_csv(data, p: Path):
    print(f"converting dataframe to CSV")
    l_df = pd.DataFrame(data)
    print(l_df)
    l_df.to_csv(p)


def revise_obsv(obs, save=False):
    record = [
        {
            'timestamp': iso_to_epoch(props['timestamp'].strip()),
            'datetime': datetime.fromisoformat(props['timestamp']).strftime("%Y/%m/%d %H:%M:%S"),
            'station_url': props['station'],
            'raw_message': props['rawMessage'].strip(),
            'description': props['textDescription'].strip(),
            'temperature_c': props['temperature']['value'],
            'dewpoint_c': props['dewpoint']['value'],
            'icon': props['icon'],
            'wind_direction': props['windDirection']['value'],
            'wind_speed_km_h': props['windSpeed']['value'],
            'wind_gust_km_h': props['windGust']['value'],
            'barometric_pressure_pa': props['barometricPressure']['value'],
            'sea_lvl_pressure_pa': props['seaLevelPressure']['value'],
            'visibility_m': props['visibility']['value'],
            'max_temp_24h_c': props['maxTemperatureLast24Hours']['value'],
            'min_temp_24h_c': props['minTemperatureLast24Hours']['value'],
            'relative_humidity': props['relativeHumidity']['value'],
            'wind_chill_c': props['windChill']['value']
        }
        for x
        in obs
        for props in [x['properties']]
    ]

    # save data snapshot to CSV
    if save:
        record_df_p = Path(
            os.path.expanduser('~'), '.databox', 'noaa', 'wx', 'forecasts',
            f"forecast_frame_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"
        )
        forecast_to_csv(record, record_df_p)

    return record


async def wx_run(loc: str, save=False):
    print(f"location: {loc}")
    coords = await async_get_lat_lng(loc.strip())
    print(f"coordinates: {coords.__str__()}")
    grid = await async_get_grid(coords[0], coords[1])
    print(f"grid: {grid.__str__()}")
    stations = await async_get_stations(grid)
    observation = await async_get_observation(stations[0]['properties']['stationIdentifier'])
    observation = revise_obsv(observation, save=True)

    # save data revision to JSON file
    if save:
        obs_json = json.dumps(observation)
        json_p = Path(
            os.path.expanduser('~'), '.databox', 'noaa',
            'wx', 'forecasts',
            f"forecast_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"
        )
        if not json_p.exists():
            json_p.parent.mkdir(parents=True, exist_ok=True)
            json_p.touch(exist_ok=True)
        with open(json_p, 'w') as f:
            print(f"writing data revision to JSON: {json_p.__str__()}")
            f.write(obs_json)
    
    return observation


def main():
    asyncio.run(wx_run('12180'))


if __name__ == "__main__":
    main()
