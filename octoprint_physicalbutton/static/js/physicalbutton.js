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
         self.gpios = ko.observableArray(['none', '4', '5', '6',
             '7', '8', '9', '10', '11', '12', '13', '16', '17',
             '18', '20', '21', '22', '23', '24', '25', '26', '27'
         ]);
         //actions:
         self.actions = ko.observableArray(['none', 'cancel', 'connect', 'disconnect', 'home', 'pause', 'resume', 'start', 'debug']);

         //button modes:
         self.buttonModes = ko.observableArray(['Normally Open (NO)', 'Normally Closed (NC)']);

         //Saved Buttons
         self.buttons = ko.observableArray();

         self.selectedGPIO = ko.observable();

         self.selectedActivity = ko.observable();
         self.index = ko.observable(1);


         self.onBeforeBinding = function() {
             self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons());
         };

         self.onSettingsBeforeSave = function() {
             self.settingsViewModel.settings.plugins.physicalbutton.buttons(self.buttons());
         };

         self.onSettingsShown = function() {
             self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons());
         };

         self.disableGpioOption = function(item, currentGPIO) {
             if (item == 'none') {
                 return false;
             }
             if (self.buttons().find(b => b.gpio() == item)) {
                 if (item != currentGPIO()) {
                     return true;
                 }
             }
             return false;
         };

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
