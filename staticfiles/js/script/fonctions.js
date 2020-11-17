function TestDelete(f1) {
    if (!confirm('Vous souhaitez supprimer ' + f1 + ' ?')) return false;
}

function TestArchive(f1) {
    if (!confirm('Vous souhaitez archiver ' + f1 + ' ?')) return false;
}

function Newpassword() {
    if (!confirm('Le nouveau mot de passe sera : sacado2020 \nIl sera envoyé directement au courriel renseigné. Confirmer ?')) return false;
}


function TestRemove(f1) {
    if (!confirm('Vous souhaitez retirer  ' + f1 + ' ?')) return false;
}




function TestDuplicate(f1) {
    if (!confirm('Vous souhaitez dupliquer ' + f1 + ' ?')) return false;
}

function TestRefus() {
    if (!confirm('Vous souhaitez refuser cette mission ?')) return false;
}

function testPassword(f1, f2) {

    f1 = document.getElementById(f1);
    f2 = document.getElementById(f2);
    if (f1.value != f2.value) {
        alert('La confirmation ne correspond pas !');
        return false;
    }
    
}


function deleteAllStudents() {
    if (!confirm('Vous souhaitez supprimer tous les élèves de votre établissement ? \nToutes leurs données actuelles seront perdues. Cette action est irréversible si vous cliquez sur OK.')) return false;
}


 
function getAllStudents() {
    if (!confirm('Vous souhaitez récupérer tous les élèves de votre établissement existant dans la base de données SACADO ? \nTous les élèves associés à un enseignant de votre établissement seront associés à votre établissement.')) return false;
}

function deleteSelectedStudents() {
    if (!confirm('Vous souhaitez supprimer tous les élèves sélectionnés ? \nToutes leurs données actuelles seront perdues. \nCette action est irréversible si vous cliquez sur OK.')) return false;
}


function changeExerciceIntoParcours() {
    if (!confirm('Vous déplacez cet exercice dans un ou plusieurs parcours. Souhaitez vous continuer ?')) return false;
}

 