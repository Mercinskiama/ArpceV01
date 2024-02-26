/*global opener */
$(function() {
    var initData = JSON.parse(document.getElementById('django-admin-popup-response-constants').dataset.popupResponse);
    opener.dismissAddRelatedObjectPopup(window, initData.value, initData.obj);
})
