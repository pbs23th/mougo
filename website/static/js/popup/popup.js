needPopup.config.custom = {
    'removerPlace': 'outside',
    'closeOnOutside': false,
    onShow: function() {
        console.log('needPopup is shown');
    },
    onHide: function() {
        console.log('needPopup is hidden');
    }
};
needPopup.init();
