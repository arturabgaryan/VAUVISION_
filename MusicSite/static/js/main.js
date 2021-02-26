function changeDetails() {
    if (document.querySelector('#arrowDown').style.display === 'none') {
        document.querySelector('#arrowDown').style.display = 'initial';
        document.querySelector('#arrowUp').style.display = 'none';
        document.querySelector('#subinfo').style.display = 'none';
    } else {

        document.querySelector('#arrowDown').style.display = 'none';
        document.querySelector('#arrowUp').style.display = 'initial';
        document.querySelector('#subinfo').style.display = 'block';
    }

}



