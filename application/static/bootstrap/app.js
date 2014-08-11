var locations = [
    ['Bondi Beach', 38.926832, -77.078819, 4],
    ['Coogee Beach', 38.920955, -77.028694, 5],
    ['Cronulla Beach', 38.891567, -77.005348, 3],
    ['Manly Beach', 38.966883, -77.036247, 2],
    ['Maroubra Beach', 38.885688, -77.107658, 1]
];

var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: new google.maps.LatLng(38.907064, -77.034874),
    mapTypeId: google.maps.MapTypeId.ROADMAP
});

var infowindow = new google.maps.InfoWindow();

var marker, i;

for (i = 0; i < locations.length; i++) {
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map
    });

    google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
            infowindow.setContent(locations[i][0]);
            infowindow.open(map, marker);
        }
    })(marker, i));
}

var nowTemp = new Date();
var now = new Date(nowTemp.getFullYear(), nowTemp.getMonth(), nowTemp.getDate(), 0, 0, 0, 0);

var checkin = $('#dpd1').datepicker({
    onRender: function(date) {
        return date.valueOf() < now.valueOf() ? '' : '';
    }
}).on('changeDate', function(ev) {
    if (ev.date.valueOf() > checkout.date.valueOf()) {
        var newDate = new Date(ev.date)
        newDate.setDate(newDate.getDate() + 1);
        checkout.setValue(newDate);
    }
    checkin.hide();
    $('#dpd2')[0].focus();
}).data('datepicker');

var checkout = $('#dpd2').datepicker({
    onRender: function(date) {
        return date.valueOf() <= checkin.date.valueOf() ? '' : '';
    }
}).on('changeDate', function(ev) {
    checkout.hide();
}).data('datepicker');