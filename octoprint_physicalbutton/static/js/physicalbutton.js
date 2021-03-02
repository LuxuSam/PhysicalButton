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

        self.buttonname = ko.observable();
        self.gpio = ko.observable();
        self.action = ko.observable();

        self.onBeforeBinding = function() {
            self.buttonname(self.settingsViewModel.settings.plugins.physicalbutton.buttonname());
            self.gpio(self.settingsViewModel.settings.plugins.physicalbutton.gpio());
            self.action(self.settingsViewModel.settings.plugins.physicalbutton.action());
        }

        self.onEventSettingsUpdated = function (payload) {
            self.buttonname(self.settingsViewModel.settings.plugins.physicalbutton.buttonname());
            self.gpio(self.settings.settingsViewModel.plugins.physicalbutton.gpio());
            self.action(self.settings.settingsViewModel.plugins.physicalbutton.action());
        }


        self.addButton = function(){

        }

        self.onSettingsShow = function() {
            //self.newName(self.settings.plugins.physicalbutton.buttonname());
        }

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
