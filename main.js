$(document).ready(function() {
    const cueBallId = 'cueBall';
    const DRAG = 150.0;
    const viewBoxWidth = 1400; // Width unit of SVG's viewBox
    const actualSvgWidth = 700;
    const pixelToSvgUnitsRatio = viewBoxWidth / actualSvgWidth;
    const VEL_EPSILON = 0.01;
    let isDragging = false;
    let startDragPosition = { x: 0, y: 0 };
    const playerName = localStorage.getItem('player1Name');

    const svg = $('#' + cueBallId).closest('svg');
    let lineElement = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    $(lineElement).attr({
        'id': 'cueLine',
        'stroke': 'black',
        'stroke-width': '10',
        'visibility': 'hidden'
    }).insertAfter('#' + cueBallId);

    $('#' + cueBallId).on('mousedown', function(event) {
        isDragging = true;
        startDragPosition.x = parseFloat($(this).attr('cx'));
        startDragPosition.y = parseFloat($(this).attr('cy'));
        updateLine(startDragPosition, startDragPosition);
        $(lineElement).attr('visibility', 'visible');
    });

    $(document).on('mousemove', function(event) {
        if (!isDragging) return;
        const currentMousePosition = getMousePosition(svg[0], event);
        updateLine(startDragPosition, currentMousePosition);
    }).on('mouseup', function(event) {
        if (!isDragging) return;
        isDragging = false;
        $(lineElement).attr('visibility', 'hidden');
        const endDragPosition = getMousePosition(svg[0], event);
        const velocity = {
            x: endDragPosition.x - startDragPosition.x,
            y: endDragPosition.y - startDragPosition.y
        };

        // Compute acceleration here if necessary
        const speed = Math.sqrt(velocity.x ** 2 + velocity.y ** 2);
        let acceleration = { x:0, y:0};
        if (speed > VEL_EPSILON){
            acceleration.x = (velocity.x / -speed) * DRAG; 
            acceleration.y = (velocity.y / -speed) * DRAG; 
        }
        //console.log('Velocity:', velocity);
        //console.log('Acceleration:', acceleration);
        sendShotData(playerName, velocity, acceleration);
        $(lineElement).remove();
        
    });

    function getMousePosition(svgElement, mouseEvent) {
        const CTM = svgElement.getScreenCTM();
        return {
            x: (mouseEvent.clientX - CTM.e) / CTM.a,
            y: (mouseEvent.clientY - CTM.f) / CTM.d
        };
    }

    function updateLine(start, end) {
        $(lineElement).attr({
            'x1': start.x,
            'y1': start.y,
            'x2': end.x,
            'y2': end.y
        });
    }

    function sendShotData(playerName, velocity, acceleration){
        const shotData = {
            playerName: playerName,
            vel_x: velocity.x,
            vel_y: velocity.y,
            acc_x: acceleration.x,
            acc_y: acceleration.y
        };

        $.ajax({
            url: '/shoot.html',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(shotData),
            dataType: 'json',
            success: function(data) {
                console.log('Success:', data);
            },
            error: function(error) {
                console.error('Error:', error);
            }
        });
    }
});
