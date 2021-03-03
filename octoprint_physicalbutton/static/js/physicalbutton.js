/*
 * View model for Physical Button
 *
 * Author: Sam
 * License: AGPLv3
 */
$(function() {
    function PhysicalbuttonViewModel(parameters) {
        var self = this;

        self.settingsViewModel = parameters[0];

        /*
        self.buttonname = ko.observable();
        self.gpio = ko.observable();
        self.action = ko.observable();
        */
        self.buttons = ko.observable();

        self.onBeforeBinding = function() {
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons());
        };

        self.onEventSettingsUpdated = function (payload) {
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons());
        }

        self.addButton = function(){
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons.push(
                {action: ko.observable('none'), buttonname:ko.observable('NewButton'), gpio: ko.observable('0')}));
            self.settingsViewModel.saveData();
        };

        self.removeButton = function(){
            self.buttons(self.settingsViewModel.settings.plugins.physicalbutton.buttons.remove(this));
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
