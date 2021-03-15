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
        self.gpios = ko.observable(['4','5','6','7','8','9','10','11','12',
                                    '13','16','17','18','20','21','22','23',
                                    '24','25','26','27']);
        //actions:
        self.actions = ko.observable(['cancel','connect','disconnect','home','pause','resume','start', 'none']);
        //button modes:
        self.buttonModes = ko.observable(['Normally Open (NO)', 'Normally Closed (NC)']);

        //New Button
        self.newButtonName   = ko.observable();
        self.newButtonGPIO   = ko.observable();
        self.newButtonMode   = ko.observable();
        self.newButtonTime   = ko.observable();
        self.checkedButton   = ko.observable();
        self.newButtonAction = ko.observable();
        self.newButtonGcode  = ko.observable();

        //Saved Buttons
        self.buttons = ko.observable();
        self.show = ko.observable();

        self.resetAddView = function() {
            self.newButtonName(null);
            self.newButtonGPIO(0);
            self.newButtonMode('Normally Open (NO)');
            self.newButtonTime(500);
            self.checkedButton(null);
            self.newButtonAction('none');
            self.newButtonGcode(null);
        }

        self.onSettingsShown = function() {
            self.resetAddView();
        }

        self.addButton = function(){
            if (self.newButtonName() == null){
                alert("You haven't chosen a name for your new button!");
                return;
            }

            if (self.checkedButton() == null) {
                alert("You haven't chosen an activity for your new button!");
                return;
            }

            if (self.settingsViewModel.settings.plugins.physicalbutton.buttons() == null){
                self.settingsViewModel.settings.plugins.physicalbutton.buttons(new Array());
                  self.settingsViewModel.saveData();
            }

            if (self.checkedButton() == "checkedGcode"){
                self.settingsViewModel.settings.plugins.physicalbutton.buttons.push(
                    {buttonname: self.newButtonName,
                        gpio: self.newButtonGPIO,
                        buttonMode: self.newButtonMode,
                        buttonTime: self.newButtonTime,
                        action: ko.observable('none'),
                        gcode: self.newButtonGcode(),
                        id: ko.observable(Date.now()),
                        show: ko.observable('gcode')});
                log.info("Added new GCODE button");
            }

            if (self.checkedButton() == "checkedAction"){
                self.settingsViewModel.settings.plugins.physicalbutton.buttons.push(
                    {buttonname: self.newButtonName,
                         gpio: self.newButtonGPIO,
                         buttonMode: self.newButtonMode,
                         buttonTime: self.newButtonTime,
                         action: self.newButtonAction,
                         gcode: ko.observable(null),
                         id: ko.observable(Date.now()),
                         show: ko.observable('action')});
                log.info("Added new Action button");
            }

            self.settingsViewModel.saveData();

            self.resetAddView();
        }

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
