namespace Gumatos.RealmApi.Skills
{
    /// <summary>
    /// Conjunto de arvores de habilidade do contrato da familia UI (inventario: `...ContractReference.Skills.SkillTree`).
    /// Enum PROPRIO da API: nao referenciamos Assembly-CSharp. O jogo tem o proprio `SkillType`;
    /// a correspondencia e por NOME (nunca por valor) e vive fora desta base (ver api/README.md, secao da familia UI).
    /// Mapeamento por nome, medido na build 1.4.8 (build 26767595):
    /// Chaos=0->SkillType.Chaos(12); Cold=1->Cold(2); Custom=2->SEM correspondencia (aba do mod);
    /// Fire=3->Fire(0); Innate=4->Innate(9); Light=5->Light(4); Lightning=6->Lightning(1);
    /// Monk=7->Monk(10); Nature=8->Nature(11); Ranger=9->Ranger(5); Shadow=10->Shadow(6);
    /// Thief=11->Thief(7); Warrior=12->Warrior(3); Bard=13->Bard(13); Basic=14->Basic(8).
    /// ATENCAO: a numeracao da API e alfabetica (legado do inventario), a do jogo e outra; a coincidencia
    /// Bard=13 nos dois lados e acidental e nao deve ser usada como contrato.
    /// </summary>
    public enum SkillTree
    {
        Chaos = 0,
        Cold = 1,
        Custom = 2,
        Fire = 3,
        Innate = 4,
        Light = 5,
        Lightning = 6,
        Monk = 7,
        Nature = 8,
        Ranger = 9,
        Shadow = 10,
        Thief = 11,
        Warrior = 12,
        // SR-BETA-06: arvores que a build 1.4.8 expoe e o inventario nao listava.
        // Acrescentadas AO FINAL para nao renumerar nada que ja era publico (mods em campo e o RSTV).
        Bard = 13,
        Basic = 14
    }
}
