namespace Gumatos.RealmApi.Skills
{
    /// <summary>
    /// Conjunto de arvores de habilidade do contrato da familia UI (inventario: `...ContractReference.Skills.SkillTree`).
    /// Enum PROPRIO da API: nao referenciamos Assembly-CSharp. O jogo tem o proprio `SkillType` (Fire=0, ... Bard=13);
    /// a correspondencia e por NOME e vive fora desta base (ver api/README.md, secao da familia UI).
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
        Warrior = 12
    }
}
