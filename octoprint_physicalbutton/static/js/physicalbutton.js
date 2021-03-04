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

        //New Button
        self.newButtonName   = ko.observable();
        self.newButtonGPIO   = ko.observable();
        self.checkedButton   = ko.observable();
        self.newButtonAction = ko.observable();
        self.newButtonGcode  = ko.observable();

        //Saved Buttons
        self.buttons = ko.observable();
        self.show = ko.observable();


        /*
        self.onBeforeBinding = function() {
            if (self.settingsViewModel.settings.plugins.physicalbutton.buttons() == null){
                return
            }
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons());
        };

        self.onEventSettingsUpdated = function (payload) {
            if (self.settingsViewModel.settings.plugins.physicalbutton.buttons() == null){
                return
            }
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons());
        }
        */
        self.addButton = function(){
            if (self.newButtonName == null){
                log.error("No Name for new button");
                return;
            }

            if (self.settingsViewModel.settings.plugins.physicalbutton.buttons() == null){
                self.settingsViewModel.settings.plugins.physicalbutton.buttons(new Array());
                self.settingsViewModel.saveData();
            }

            if (self.checkedButton() == "checkedGcode"){
                log.info("Added new GCODE button");

                self.settingsViewModel.settings.plugins.physicalbutton.buttons.push(
                    {buttonname:self.newButtonName, gpio: self.newButtonGPIO, action: ko.observable(null), gcode: self.newButtonGcode, id: ko.observable(Date.now()), show: ko.observable('gcode')});
                self.settingsViewModel.saveData();
            }

            if (self.checkedButton() == "checkedAction"){
                log.info("Added new Action button");

                self.settingsViewModel.settings.plugins.physicalbutton.buttons.push(
                    {buttonname:self.newButtonName, gpio: self.newButtonGPIO, action: self.newButtonAction, gcode: ko.observable(null), id: ko.observable(Date.now()), show: ko.observable('action')});
                self.settingsViewModel.saveData();
            }

            self.newButtonName(null);
            self.newButtonGPIO(0);
            self.checkedButton(null);
            self.newButtonAction('none');
            self.newButtonGcode(null);
        };

        self.removeButton = function(){
            self.settingsViewModel.settings.plugins.physicalbutton.buttons.remove(this);
            self.settingsViewModel.saveData();
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
