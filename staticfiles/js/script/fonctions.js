/* code réalisé par Philippe Demaria - tout droit réservé */
/* code pour sacado */

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


    var checked_groups = document.getElementsByClassName("select_all") ; 
    var leng = 0 ;
    for(let i = 0; i < checked_groups.length ; i++) {
        if(checked_groups[i].checked) {
          leng++;
        }
    }

    if (leng == 0) {
            if (!confirm("Vous devriez sélectionner au moins un groupe. Confirmez l'enregistrement sans groupe ?")) return false ;             
            } 
}


function test_aefe() {
    if (!confirm("Vous devez avoir vos groupes entièrement constitués avant de procéder à l'attribution. Sinon vous devrez réattribuer les élèves manquants. Confirmer l'attribution ?")) return false;
}


function check_checkboxes()
{
  var c = document.getElementsByClassName('folder_line');
  for (var i = 0; i < c.length; i++)
  {
    if (c[i].type == 'checkbox')
    {
       if (c[i].checked) {return true}
    }
  }
  return false;
}

function TestDeleteFolder(f1) {
    if (!confirm('Vous souhaitez supprimer ' + f1 + ' ?')) return false;

    if(check_checkboxes())
        {
            alert("Vous devez décocher les parcours de ce dossier et l'enregistrer sans parcours associés. Alors vous pourrez le supprimer dans un second temps.");  
            return false;
        }
        return true;

}


function delete_all_these_groups(f) {
     if (!confirm('Vous souhaitez supprimer '+f+' ? \nToutes leurs données actuelles seront perdues. \nCette action est irréversible si vous cliquez sur OK.')) return false;
 }


function ebepSelectedStudents(f) {
     if (!confirm('Vous souhaitez attribuer/retirer les outils inclusifs à '+f+' ?')) return false;
 }