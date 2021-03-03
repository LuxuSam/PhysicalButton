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
        self.newButtonName = ko.observable();
        self.newButtonGPIO = ko.observable();
        self.checkedButton = ko.observable();
        self.newButtonAction = ko.observable();
        self.newButtonGcode = ko.observable();

        //Saved Buttons
        self.buttons = ko.observable();

        self.onBeforeBinding = function() {
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons());
        };

        self.onEventSettingsUpdated = function (payload) {
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons());
        }

        self.addButton = function(){
            if (self.newButtonName == null){
                console.log("No Name");
                return;
            }
            if (self.checkedButton() == "checkedGcode"){
                console.log("Not implemented yet");
                return;
            }
            if (self.checkedButton() == "checkedAction"){
                console.log("Added Action Button");
                self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons.push(
                    {action: self.newButtonAction, buttonname:self.newButtonName, gpio: self.newButtonGPIO}));
                self.settingsViewModel.saveData();
                ;
            }
        };

        self.removeButton = function(){
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons.remove(this));
            //self.settingsViewModel.saveData();

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
