import os
from quart import Quart, render_template, jsonify, request
import asyncio
import json
from datetime import datetime, timezone
import pytz
from collections import OrderedDict

app = Quart(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


async def get_script_output(client_timezone):
    utc_now = datetime.now(timezone.utc)
    
    # Convert to the client's timezone
    local_tz = pytz.timezone(client_timezone)
    client_time = utc_now.astimezone(local_tz)
    client_time_str = client_time.isoformat()
    print("\nthe client time is", client_time_str)
    
    process = await asyncio.create_subprocess_exec(
        'python', 'script.py', utc_now.isoformat(), client_timezone,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()
    if stderr:
        print(f"Error: {stderr.decode()}")

    sorted_data = sorted(json.loads(stdout.decode()).items(), key=lambda x: x[1]['next'])
    
    # Convert sorted_data back to a dictionary
    sorted_dict = OrderedDict((key, value) for key, value in sorted_data)
    return sorted_dict

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/collab')
async def collab():
    return await render_template('collab.html')

@app.route('/get_data')
async def get_data():
    client_timezone = request.args.get('timezone', 'UTC')  # Default to UTC if no timezone is provided
    print(client_timezone)
    output = await get_script_output(client_timezone)
    
    ordered_list = [{'key': key, **value} for key, value in output.items()]
    print(ordered_list)
    return jsonify(ordered_list)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
