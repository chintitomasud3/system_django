import psutil
import platform
from django.shortcuts import render

def system_dashboard(request):
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    virtual_mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage('/')
    net_io = psutil.net_io_counters()
    boot_time = psutil.boot_time()
    
    system_info = {
        'system': platform.system(),
        'node': platform.node(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
    }
    
    stats = {
        'cpu': {
            'percent': cpu_percent,
            'count': cpu_count,
            'current_freq': round(cpu_freq.current, 2) if cpu_freq else None,
            'max_freq': round(cpu_freq.max, 2) if cpu_freq else None,
        },
        'memory': {
            'total': round(virtual_mem.total / (1024**3), 2),
            'available': round(virtual_mem.available / (1024**3), 2),
            'used': round(virtual_mem.used / (1024**3), 2),
            'percent': virtual_mem.percent,
        },
        'swap': {
            'total': round(swap.total / (1024**3), 2),
            'used': round(swap.used / (1024**3), 2),
            'percent': swap.percent,
        },
        'disk': {
            'total': round(disk.total / (1024**3), 2),
            'used': round(disk.used / (1024**3), 2),
            'free': round(disk.free / (1024**3), 2),
            'percent': disk.percent,
        },
        'network': {
            'bytes_sent': round(net_io.bytes_sent / (1024**2), 2),
            'bytes_recv': round(net_io.bytes_recv / (1024**2), 2),
        },
        'boot_time': boot_time,
    }
    
    return render(request, 'system_info/dashboard.html', {
        'system_info': system_info,
        'stats': stats,
    })