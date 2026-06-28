function uploadFile(){

    const file=document.getElementById("fileInput").files[0];

    if(!file){

        alert("Please choose a file");

        return;

    }

    document.getElementById("output").innerHTML=`

    <h3>Record Processed</h3>

    <p><b>File Name:</b> ${file.name}</p>

    <p><b>Status:</b> Ready for Backend Processing</p>

    `;

}