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

 
