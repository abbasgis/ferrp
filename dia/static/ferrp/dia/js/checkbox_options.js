/**
 * Created by Mariam on 2/16/2019.
 */

function checkboxOption() {
    // get reference to element containing toppings checkboxes
var el = document.getElementById('id_recongized_hazard');

// get reference to input elements in toppings container element
var tops = el.getElementsByTagName('input');

// assign function to onclick property of each checkbox
for (var i=0, len=tops.length; i<len; i++) {
    if ( tops[i].type === 'checkbox' ) {
        tops[i].onclick = function() {
            if ( this.checked ) {
            val=this.value;
             if (val == "earthquake") {
              document.getElementById(val).style.display = "block";

             alert(val);

            }
            if (val == "landslide") {
                document.getElementById(val).style.display = "block";
                alert(val);

            }
            if (val == "flood") {
                document.getElementById(val).style.display = "block";
                alert(val);

            }
            if (val == "GLOF") {
                document.getElementById(val).style.display = "block";
                alert(val);

            }
            if (val == "slope_failure") {
                document.getElementById(val).style.display = "block";
                alert(val);

            }
            if (val == "heavy_rain") {
                document.getElementById(val).style.display = "block";
                alert(val);

            }
            if (val == "strong_wind") {
                document.getElementById(val).style.display = "block";
                alert(val);

            }
    }
    else
    {
        if(!this.checked)
        {
            val=this.value;
             if (val == "earthquake") {
              document.getElementById(val).style.display = "none";
             alert("earthquake uncheck"+val);

            }
            if (val == "landslide") {
                document.getElementById(val).style.display = "none";
                alert("uncheck"+val);

            }
            if (val == "flood") {
                document.getElementById(val).style.display = "none";
                alert("uncheck"+val);

            }
            if (val == "GLOF") {
                document.getElementById(val).style.display = "none";


            }
            if (val == "slope_failure") {
                document.getElementById(val).style.display = "none";


            }
            if (val == "heavy_rain") {
                document.getElementById(val).style.display = "none";


            }
            if (val == "strong_wind") {
                document.getElementById(val).style.display = "none";

            }

        }
    }
        }
    }
}

}
