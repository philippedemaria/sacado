function TestDelete(f1) {
    if (!confirm('Vous souhaitez supprimer ' + f1 + ' ?')) return false;
}

function Newpassword() {
    if (!confirm('Vous souhaitez créer un nouveau mot de passe ? ce sera : sacado2020')) return false;
}



function TestDuplicate(f1) {
    if (!confirm('Vous souhaitez dupliquer ' + f1 + ' ?')) return false;
}

function TestRefus() {
    if (!confirm('Vous souhaitez Refuser cette mission ?')) return false;
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
    if (!confirm('Vous souhaitez supprimer tous les élèves de votre établissement ? Toutes leurs données actuelles seront perdues. Cette action est irréversible si vous cliquer sur OK.')) return false;
}


 
function getAllStudents() {
    if (!confirm('Vous souhaitez récupérer tous les élèves de votre établissement existant dans la base de données SACADO ? Tous les élèves associés à un enseignant de votre établissement seront associés à votre établissement.')) return false;
}