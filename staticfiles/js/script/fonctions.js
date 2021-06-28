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


function TestRenew() {
    if (!confirm("Vous souhaitez renouveler la cotisation ? En cliquant, vous créez un devis et pourrez choisir le mode de réglement qui vous convient. Une fois la cotisation reçue, nous enclenchons la version établissement." )) return false;
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



function get_this_confirmation(f1) {
    if (!confirm('Vous souhaitez récupérer ' + f1 + ' ?')) return false;
}
 

function check_if_checked() {

    var checkeds = document.getElementsByClassName("check_if_check") ;
    var len = 0 ;
    for(let i = 0; i < checkeds.length ; i++) {
        if(checkeds[i].checked) {
          len++;
        }
    }
    if (len == 0) {
            if (!confirm("Vous devriez sélectionner au moins un élève. Si vous n'avez pas encore d'élèves, créez-vous un profil élève dans chacun de vos groupes. Confirmez l'enregistrement sans élève ?")) return false ;             
            } 
}


function test_aefe() {
    if (!confirm("Vous devez avoir vos groupes entièrement constitués avant de procéder à l'attribution. Sinon vous devrez réattribuer les élèves manquants. Confirmer l'attribution ?")) return false;
}
