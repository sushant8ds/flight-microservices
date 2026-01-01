document.addEventListener("DOMContentLoaded", () => {
    flight_duration2();
    filter_price2();
    document.querySelector(".clr-filter-div2 button").addEventListener('click', reset_filter2);
});

function flight_duration2() {
    document.querySelectorAll(".flight-stops2 .tooltiptext").forEach(element => {
        let time = element.dataset.value.split(":");
        element.innerText = time[0]+"h "+time[1]+"m";
    });
}

function filter_price2() {
    let value = document.querySelector(".filter-price2 input[type=range]").value;
    document.querySelector(".filter-price2 .final-price-value").innerText = value;

    let div = document.querySelector("#flights_div2");
    let flights = div.querySelectorAll(".each-flight-div-box");
    for (let i = 0; i < flights.length; i++) {
        if (flights[i].querySelector(".flight-price span").innerText > parseInt(value)) {
            flights[i].classList.add('hide');
            flights[i].classList.remove('show');
        }
        else {
            flights[i].classList.add('show');
            flights[i].classList.remove('hide');
        }
    }
}

function reset_filter2() {
    document.querySelectorAll('.time-slot2').forEach(slot => {
        inactive2(slot.querySelector(".square-box.active"));
    });
    let max = document.querySelector(".filter-price2 input[type=range]").getAttribute('max');
    document.querySelector(".filter-price2 input[type=range]").value = max;
    document.querySelector(".filter-price2 .final-price-value").innerText = max;

    let flights = document.querySelector("#flights_div2").querySelectorAll(".each-flight-div-box");
    for (let i = 0; i < flights.length; i++) {
        flights[i].classList.add('show');
        flights[i].classList.remove('hide');
    }
}
document.addEventListener('DOMContentLoaded', () => {
    let ref1 = document.querySelector(".ref1").value;
    let ref2 = document.querySelector(".ref2").value;
    setTimeout(() => {
        fetch(`/flight/ticket/api/${ref1}`)
        .then(response => response.json())
        .then(ticket1 => {
            if(ref2) {
                fetch(`/flight/ticket/api/${ref2}`)
                .then(response => response.json())
                .then(ticket2 => {
                    if (ticket2.status === 'CONFIRMED') {
                        document.querySelector(".section2 .flight2 .ref").innerText = ticket2.ref;
                        document.querySelector(".section2 .flight2 .from2").innerText = ticket2.from;
                        document.querySelector(".section2 .flight2 .to2").innerText = ticket2.to;
                        document.querySelector(".flight2").style.display = 'block';
                    }
                    else {
                        throw Error(ticket2.status);
                    }
                });
            }
            if (ticket1.status === 'CONFIRMED') {
                document.querySelector(".section2 .flight1 .ref").innerText = ticket1.ref;
                document.querySelector(".section2 .flight1 .from1").innerText = ticket1.from;
                document.querySelector(".section2 .flight1 .to1").innerText = ticket1.to;
            }
            else {
                throw Error(ticket1.status);
            }
        })
        .then(() => {
            document.querySelector(".section1").style.display = 'none';
            document.querySelector(".section2").style.display = 'block';
            document.querySelector(".section3").style.display = 'none';
            //document.querySelector(".section2 svg").style.animationPlayState = 'running';
        })
        .catch(() => {
            document.querySelector(".section1").style.display = 'none';
            document.querySelector(".section2").style.display = 'none';
            document.querySelector(".section3").style.display = 'block';
        })
    }, 2000);
})