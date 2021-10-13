/*
 * View model for Physical Button
 *
 * Author: Sam
 * License: AGPLv3
 */
$(function() {
    function PhysicalbuttonViewModel(parameters) {
        var self = this;

        //settings
        self.settingsViewModel = parameters[0];

         //GPIOs:
         self.gpios = ko.observableArray(['none', '2', '3', '4', '5', '6',
             '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
             '18', '19', '20', '21', '22', '23', '24', '25', '26', '27'
         ]);
         //actions:
         self.actions = ko.observableArray(['none', 'connect', 'disconnect', 'home', 'pause', 'resume', 'toggle pause-resume', 'start', 'start latest', 'cancel', 'toggle start-cancel']);

        //button modes:
        self.buttonModes = ko.observableArray(['Normally Open (NO)', 'Normally Closed (NC)']);

        //Saved Buttons
        self.buttons = ko.observableArray();

        self.selectedGPIO = ko.observable();

        self.selectedActivity = ko.observable();
        self.index = ko.observable(1);

        self.changeDetected = ko.observable(false);

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

        self.viewChanged = function(obj, event) {
            if (event.originalEvent) { //user changed
                self.changeDetected(true);
            }
        }

        self.disableGpioOption = function(item, currentGPIO) {
            if (item == 'none' || item == currentGPIO())
                return false;

            //disable used input gpios
            if (self.buttons().find(b => b.gpio() == item))
                return true;

            //disable used output gpios
            if (self.buttons().find(b => b.activities().find(a => a.type() == 'output' && a.execute.gpio() == item)))
                return true;

            return false;
        };

        self.disableGpioOutputOption = function(item){
            if (item == 'none')
                return false;

            //disable used input gpios
            if (self.buttons().find(b => b.gpio() == item))
                return true;
        }

        self.addButton = function() {
            if (!self.buttons()) {
                self.buttons(new Array());
            }
            self.buttons.push({
                activities: ko.observableArray(new Array()),
                buttonMode: ko.observable('Normally Open (NO)'),
                buttonName: ko.observable('New Button Name'),
                gpio: ko.observable('none'),
                buttonTime: ko.observable('500'),
                id: ko.observable(Date.now())
            });
        };

        self.removeButton = function() {
            self.buttons.remove(this)
        };

        self.addAction = function() {
            var updatedItem = this;
            if (!updatedItem.activities()) {
                updatedItem.activities(new Array);
            }
            updatedItem.activities.push({
                type: ko.observable('action'),
                identifier: ko.observable('New Action'),
                execute: ko.observable('none')
            });
            self.selectedActivity(this.activities()[this.activities().length - 1]);
        };

        self.addGCODE = function() {
            var updatedItem = this;
            if (!updatedItem.activities()) {
                updatedItem.activities(new Array);
            }
            updatedItem.activities.push({
                type: ko.observable('gcode'),
                identifier: ko.observable('New GCODE'),
                execute: ko.observable('')
            });
            self.selectedActivity(this.activities()[this.activities().length - 1]);
        };

        self.addSystem = function() {
            var updatedItem = this;
            if (!updatedItem.activities()) {
                updatedItem.activities(new Array);
            }
            updatedItem.activities.push({
                type: ko.observable('system'),
                identifier: ko.observable('New System Command'),
                execute: ko.observable('')
            });
            self.selectedActivity(this.activities()[this.activities().length - 1]);
        };

        self.addFile = function() {
            var updatedItem = this;
            if (!updatedItem.activities()) {
                updatedItem.activities(new Array);
            }
            updatedItem.activities.push({
                type: ko.observable('file'),
                identifier: ko.observable('New File'),
                execute: ko.observable('')
            });
            self.selectedActivity(this.activities()[this.activities().length - 1]);
        };

        self.addOutput = function() {
            var updatedItem = this;
            if (!updatedItem.activities()) {
                updatedItem.activities(new Array);
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

        self.actionChanged = function(action, data, event){
            if(event.originalEvent && self.selectedActivity().type() == 'action'){
                var identifier = self.selectedActivity().identifier();
                if (identifier == 'New Action' || self.actions().includes(identifier) || identifier.replace(/\s/g, "") == '') {
                    self.selectedActivity().identifier(self.selectedActivity().execute());
                }
            }
        }

        self.initialValueChanged = function(initialValue, gpio, id, data, event){
            if (gpio == 'none'){
                return;
            }
            if (event.originalEvent) { //user changed
                if (initialValue == 'HIGH'){ //toggle value as old initial value is passed
                    initialValue = 'LOW'
                }else{
                    initialValue = 'HIGH'
                }
                for (let button of self.buttons()){ //set all initial values for this gpio to the new initial value
                    for (let activity of button.activities()){
                        if (activity.type() == 'output' && activity.execute.id() != id && activity.execute.gpio() != 'none' && activity.execute.gpio() == gpio){
                            activity.execute.initial(initialValue);
                        }
                    }
                }
            }
        }

        self.outputGpioChanged = function(gpio, id, data, event){
            if (gpio == 'none'){
                return;
            }
            console.log(event.originalEvent);
            if (event.originalEvent) {
                for (let button of self.buttons()){ //set all initial values for this gpio to the new initial value
                    const activity = button.activities().find(activity => activity.type() == 'output' && activity.execute.id() != id && activity.execute.gpio() != 'none' && activity.execute.gpio() == gpio)
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
            for (var i = 0; i < spliced.length; i++) {
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
