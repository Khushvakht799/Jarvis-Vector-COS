// launcher-gui/src/main.js
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

class ServiceManager {
    constructor() {
        this.services = {
            'python-brain': { process: null, port: 8000, status: 'stopped' },
            'go-service': { process: null, port: 8081, status: 'stopped' },
            'node-api': { process: null, port: 3001, status: 'stopped' }
        };
    }

    startService(serviceName) {
        const service = this.services[serviceName];
        
        return new Promise((resolve, reject) => {
            let command, args, cwd;
            
            switch(serviceName) {
                case 'python-brain':
                    cwd = path.join(__dirname, '../../brain_service');
                    command = 'python';
                    args = ['src/app.py'];
                    break;
                case 'go-service':
                    cwd = path.join(__dirname, '../../i2_go');
                    command = 'go';
                    args = ['run', 'main.go'];
                    break;
                case 'node-api':
                    cwd = path.join(__dirname, '../../i1_api');
                    command = 'npm';
                    args = ['run', 'dev'];
                    break;
            }

            service.process = spawn(command, args, { cwd, stdio: 'pipe' });
            
            service.process.stdout.on('data', (data) => {
                console.log(`[${serviceName}] ${data}`);
                // Отправляем логи в GUI
                mainWindow.webContents.send('service-log', {
                    service: serviceName,
                    message: data.toString()
                });
            });

            service.process.stderr.on('data', (data) => {
                console.error(`[${serviceName} ERROR] ${data}`);
                mainWindow.webContents.send('service-error', {
                    service: serviceName,
                    message: data.toString()
                });
            });

            service.process.on('close', (code) => {
                service.status = 'stopped';
                mainWindow.webContents.send('service-status', {
                    service: serviceName,
                    status: 'stopped'
                });
            });

            // Ждем пока сервис запустится
            setTimeout(() => {
                service.status = 'running';
                mainWindow.webContents.send('service-status', {
                    service: serviceName,
                    status: 'running'
                });
                resolve();
            }, 3000);
        });
    }

    stopService(serviceName) {
        const service = this.services[serviceName];
        if (service.process) {
            service.process.kill();
            service.status = 'stopped';
        }
    }

    async startAll() {
        for (const serviceName in this.services) {
            await this.startService(serviceName);
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }

    stopAll() {
        for (const serviceName in this.services) {
            this.stopService(serviceName);
        }
    }
}

const serviceManager = new ServiceManager();
let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false
        }
    });

    mainWindow.loadFile('src/index.html');
    
    // Открываем DevTools в режиме разработки
    if (process.argv.includes('--dev')) {
        mainWindow.webContents.openDevTools();
    }
}

// IPC обработчики
ipcMain.handle('start-service', async (event, serviceName) => {
    await serviceManager.startService(serviceName);
});

ipcMain.handle('stop-service', (event, serviceName) => {
    serviceManager.stopService(serviceName);
});

ipcMain.handle('start-all', async () => {
    await serviceManager.startAll();
});

ipcMain.handle('stop-all', () => {
    serviceManager.stopAll();
});

app.whenReady().then(createWindow);