/*
 * View model for Physical Button
 *
 * Author: Sam
 * License: AGPLv3
 */
$(function() {
    function PhysicalbuttonViewModel(parameters) {
        let self = this;

        //settings
        self.settingsViewModel = parameters[0];

         //GPIOs:
         self.gpios = ko.observableArray(['none', '2', '3', '4', '5', '6',
             '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
             '18', '19', '20', '21', '22', '23', '24', '25', '26', '27'
         ]);

         //actions:
         self.actions = ko.observableArray(['none', 'connect', 'disconnect', 'home', 'pause', 'resume', 'toggle pause-resume',
                                            'start', 'start latest', 'cancel', 'toggle start-cancel', 'toggle start latest-cancel', 'unselect file']);

        //button modes:
        self.buttonModes = ko.observableArray(['Normally Open (NO)', 'Normally Closed (NC)']);

        //output options:
        self.outputOptions = ko.observableArray(['HIGH', 'LOW', 'Toggle']);

        //supported Plugin:
        self.supportedPlugins = ko.observableArray([]);

        //Saved Buttons
        self.buttons = ko.observableArray();

        self.selectedGPIO = ko.observable();

        self.selectedActivity = ko.observable();
        self.index = ko.observable(1);

        self.changeDetected = ko.observable(false);

        self.uploadedConfig = ko.observableArray();

        self.missingProperty = ko.observableArray([]);

        self.onBeforeBinding = function() {
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons());
        };

        self.onSettingsBeforeSave = function() {
            self.settingsViewModel.settings.plugins.physicalbutton.buttons(self.buttons());
            self.changeDetected(false);
        };

        self.onSettingsShown = function() {
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons());
        };

        self.onDataUpdaterPluginMessage = function (plugin, message){
            if(plugin !== "physicalbutton")
                return;
            self.supportedPlugins(message);
        };

        self.viewChanged = function(obj, event) {
            if (event.originalEvent) { //user changed
                self.changeDetected(true);
            }
        }

        self.disableGpioOption = function(item, currentGPIO) {
            if (item === 'none' || item === currentGPIO())
                return false;

            //disable used input GPIOs
            if (self.buttons().find(b => b.gpio() === item))
                return true;

            //disable used output GPIOs
            if (self.buttons().find(b => b.activities().find(a => a.type() === 'output' && a.execute.gpio() === item)))
                return true;

            return false;
        };

        self.disableGpioOutputOption = function(item){
            if (item === 'none')
                return false;

            //disable used input GPIOs
            if (self.buttons().find(b => b.gpio() === item))
                return true;
        }

        self.addButton = function() {
            if (!self.buttons()) {
                self.buttons([]);
            }
            self.buttons.push({
                activities: ko.observableArray([]),
                buttonMode: ko.observable('Normally Open (NO)'),
                buttonName: ko.observable('New Button Name'),
                enabled: ko.observable(true),
                enabledWhilePrinting: ko.observable(true),
                gpio: ko.observable('none'),
                buttonTime: ko.observable('500'),
                id: ko.observable(Date.now())
            });
        };

        self.downloadConfig = function() {
            const element = document.createElement('a');
            element.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(ko.toJSON(self.buttons, null, 2)));
            element.setAttribute('download', 'button_config');

            element.style.display = 'none';
            document.body.appendChild(element);

            element.click();
            document.body.removeChild(element);
        }

        self.checkUpload = function (file){
            self.uploadedConfig(ko.mapping.fromJS(file)());
            self.missingProperty([]);
            // check if config has needed keys
            let properties = ['activities', 'buttonMode', 'buttonName', 'enabled', 'enabledWhilePrinting', 'gpio', 'buttonTime', 'id'];
            for (let b = 0; b < self.uploadedConfig().length; b++) {
                for (let p = 0; p < properties.length; p++) {
                    if (!self.uploadedConfig()[b].hasOwnProperty(properties[p])) {
                        self.missingProperty([properties[p],b]);
                        self.uploadedConfig([]);
                        return;
                    }
                }
            }
        }

        self.fileUploaded = function(data, event) {
            let file    = event.target.files[0];
            let reader  = new FileReader();
            reader.onload = function (onload_e)
            {
                if (typeof reader.result === 'string')
                    self.checkUpload(JSON.parse(reader.result));
            };
            if (file){
                reader.readAsText(file);
            }
        }
        
        self.saveConfig = function () {
            // Save data into buttons
            if (self.uploadedConfig().length > 0){
                self.buttons(self.uploadedConfig());
            }

            self.changeDetected(true);
            self.uploadedConfig([]);
        }

        self.removeButton = function() {
            self.buttons.remove(this)
        };

        self.addAction = function() {
            let updatedItem = this;
            if (!updatedItem.activities()) {
                updatedItem.activities([]);
            }
            updatedItem.activities.push({
                type: ko.observable('action'),
                identifier: ko.observable('New Action'),
                execute: ko.observable('none')
            });
            self.selectedActivity(this.activities()[this.activities().length - 1]);
        };

        self.addGCODE = function() {
            let updatedItem = this;
            if (!updatedItem.activities()) {
                updatedItem.activities([]);
            }
            updatedItem.activities.push({
                type: ko.observable('gcode'),
                identifier: ko.observable('New GCODE'),
                execute: ko.observable('')
            });
            self.selectedActivity(this.activities()[this.activities().length - 1]);
        };

        self.addSystem = function() {
            let updatedItem = this;
            if (!updatedItem.activities()) {
                updatedItem.activities([]);
            }
            updatedItem.activities.push({
                type: ko.observable('system'),
                identifier: ko.observable('New System Command'),
                execute: ko.observable('')
            });
            self.selectedActivity(this.activities()[this.activities().length - 1]);
        };

        self.addFile = function() {
            let updatedItem = this;
            if (!updatedItem.activities()) {
                updatedItem.activities([]);
            }
            updatedItem.activities.push({
                type: ko.observable('file'),
                identifier: ko.observable('New File'),
                execute: ko.observable('')
            });
            self.selectedActivity(this.activities()[this.activities().length - 1]);
        };

        self.addOutput = function() {
            let updatedItem = this;
            if (!updatedItem.activities()) {
                updatedItem.activities([]);
            }
            updatedItem.activities.push({
                type: ko.observable('output'),
                identifier: ko.observable('New Output'),
                execute: {
                    gpio: ko.observable('none'),
                    value: ko.observable('HIGH'),
                    time: ko.observable('500'),
                    async: ko.observable('False'),
                    initial: ko.observable('LOW'),
                    id: ko.observable(Date.now())
                }
            });
            self.selectedActivity(this.activities()[this.activities().length - 1]);
        }

        self.addPluginAction = function(){
            let updatedItem = this
            if (!updatedItem.activities()) {
                updatedItem.activities([]);
            }
            updatedItem.activities.push({
                type: ko.observable('plugin'),
                identifier: ko.observable('New Plugin Action'),
                execute: {
                    plugin: ko.observable("none"),
                    action: ko.observable('none')
                }
            });
            self.selectedActivity(updatedItem.activities()[updatedItem.activities().length - 1]);
        }

        self.activityChanged = function(data, event){
            if(event.originalEvent){
                const identifier = self.selectedActivity().identifier();
                if(self.selectedActivity().type() === 'action'){
                    if (identifier === 'New Action' || identifier.replace(/\s/g, "") === '' || self.actions().includes(identifier)) {
                        const execute = self.selectedActivity().execute();
                        self.selectedActivity().identifier(execute);
                    }
                    return;
                }

                if(self.selectedActivity().type() === 'gcode'){
                    if (identifier === 'New GCODE' || identifier.replace(/\s/g, "") === ''){
                        const execute = self.selectedActivity().execute().split('\n');
                        const first = execute[0];

                        self.selectedActivity().identifier(first);
                    }
                    return;
                }

                if(self.selectedActivity().type() === 'system'){
                    if (identifier === 'New System Command' || identifier.replace(/\s/g, "") === ''){
                        const execute = self.selectedActivity().execute().split('\n');
                        const first = execute[0];
                        self.selectedActivity().identifier(first);
                    }
                    return;
                }

                if(self.selectedActivity().type() === 'file'){
                    const fileFormats = ['s3g', 'x3d','gcode', 'gco', 'g']

                    if (identifier === 'New File' || identifier.replace(/\s/g, "") === ''
                        || fileFormats.map(x => identifier.split('.')[identifier.split('.').length -1] === x).reduce((prev, curr) => prev || curr)){
                        const execute = self.selectedActivity().execute().split('/');
                        const file = execute[execute.length -1];

                        if (fileFormats.map(x => file.split('.')[file.split('.').length-1] === x).reduce((prev, curr) => prev || curr)){
                            self.selectedActivity().identifier(file);
                        }
                    }
                    return;
                }

                if(self.selectedActivity().type() === 'output'){
                    if (identifier === 'New Output' || identifier.replace(/\s/g, "") === '' || identifier.includes('GPIO none') ||(identifier.includes('GPIO') && identifier.includes('-') && identifier.includes('ms'))){
                        const gpio = self.selectedActivity().execute.gpio();
                        let value = self.selectedActivity().execute.value();
                        value = value[0] + value.substring(1).toLowerCase();
                        const time = self.selectedActivity().execute.time();
                        let newIdentifier = 'GPIO' + gpio + '-' + value + '-' + time + 'ms'
                        if (gpio === 'none'){
                            newIdentifier = 'GPIO none';
                        }
                        self.selectedActivity().identifier(newIdentifier);

                    }
                    return;
                }

                if (self.selectedActivity().type() == 'plugin') {
                    let plugin = identifier.split(': ').length > 1 ? identifier.split(': ')[0] : '';
                    let action = identifier.split(': ').length > 1 ? identifier.split(': ')[1] : '';
                    if (identifier === 'New Plugin Action' || identifier.replace(/\s/g, "") === '' || (Object.keys(self.supportedPlugins()).includes(plugin) && self.supportedPlugins()[plugin].includes(action))) {
                        let newIdentifier = self.selectedActivity().execute.plugin() + ': ' + self.selectedActivity().execute.action();
                        self.selectedActivity().identifier(newIdentifier);
                    }
                    return;
                }

            }
        }

        self.initialValueChanged = function(initialValue, gpio, id, data, event){
            if (gpio === 'none'){
                return;
            }
            if (event.originalEvent) { //user changed
                if (initialValue === 'HIGH'){ //toggle value as old initial value is passed
                    initialValue = 'LOW'
                }else{
                    initialValue = 'HIGH'
                }
                for (let button of self.buttons()){ //set all initial values for this gpio to the new initial value
                    for (let activity of button.activities()){
                        if (activity.type() === 'output' && activity.execute.id() !== id && activity.execute.gpio() !== 'none' && activity.execute.gpio() === gpio){
                            activity.execute.initial(initialValue);
                        }
                    }
                }
            }
        }

        self.outputGpioChanged = function(gpio, id, data, event){
            if (gpio === 'none'){
                return;
            }
            if (event.originalEvent) {
                for (let button of self.buttons()){ //set initial value if it was already set for this gpio
                    const activity = button.activities().find(activity => activity.type() === 'output' && activity.execute.id() !== id && activity.execute.gpio() !== 'none' && activity.execute.gpio() === gpio)
                    if (activity){
                        self.selectedActivity().execute.initial(activity.execute.initial());
                        return;
                    }
                }
            }
        }

        self.removeActivity = function() {
            if (!self.selectedActivity()) {
                return;
            }
            this.activities.remove(self.selectedActivity());
            self.selectedActivity(this.activities()[this.activities().length - 1]);
        };

        self.changeSelection = function() {
            self.selectedActivity(this.activities()[0]);
        };

        self.updatePosition = function() {
            const length = this.activities().length
            if (length < 2)
                return;
            if (self.index() < 1) {
                self.index(1)
            }
            if (self.index() > length) {
                self.index(length)
            }
            const current = self.selectedActivity();
            const amount = length - self.index();
            this.activities.remove(current);
            const spliced = this.activities.splice(self.index() - 1, amount);
            this.activities.push(current);
            for (let i = 0; i < spliced.length; i++) {
                this.activities.push(spliced[i]);
            }
            self.index(1)
        };
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: PhysicalbuttonViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: ["settingsViewModel"],
        // Elements to bind to, e.g. #settings_plugin_physicalbutton, #tab_plugin_physicalbutton, ...
        elements: ["#settings_plugin_physicalbutton"]
    });
});
