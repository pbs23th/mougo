// function onoff() {
//     console.log()
//     fetch('/onoff', {
//         method: 'POST',
//         body: JSON.stringify(),
//     }).then((_res) => {
//         window.location.href = "/";
//     });
// }

function change() // no ';' here
{
    console.log('data2');
    console.log(this.value);
    // if(data.value=="on") {
    //     console.log(data.value)
    //     data.value = "off"
    // } else {
    //     console.log(data.value)
    //     data.value = "on"
    // }
    // if (this.value=="Close Curtain") this.value = "Open Curtain";
    // else this.value = "Close Curtain";
}



// function deleteNote(noteId) {
//     fetch('/delete-note', {
//         method: 'POST',
//         body: JSON.stringify({ noteId: noteId }),
//     }).then((_res) => {
//         window.location.href = "/";
//     });
// }