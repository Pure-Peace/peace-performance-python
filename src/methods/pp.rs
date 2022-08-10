use rosu_pp::{
    AnyPP, Beatmap as RawBeatmap, CatchPP, DifficultyAttributes, ManiaPP, OsuPP,
    PerformanceAttributes, TaikoPP,
};

#[derive(Clone, Debug)]
pub struct PpRaw {
    pub aim: Option<f32>,
    pub spd: Option<f32>,
    pub str: Option<f32>,
    pub acc: Option<f32>,
    pub total: f32,
}

impl PpRaw {
    #[inline]
    pub fn new(
        aim: Option<f32>,
        spd: Option<f32>,
        str: Option<f32>,
        acc: Option<f32>,
        total: f32,
    ) -> Self {
        Self {
            aim,
            spd,
            str,
            acc,
            total,
        }
    }
}

/// Basic struct containing the result of a PP calculation.
#[derive(Clone, Debug)]
pub struct PpResult {
    pub mode: u8,
    pub mods: u32,
    pub pp: f64,
    pub raw: PerformanceAttributes,
    pub attributes: DifficultyAttributes,
}

impl PpResult {
    /// The final pp value.
    #[inline]
    pub fn pp(&self) -> f64 {
        self.pp
    }

    /// The final star value.
    #[inline]
    pub fn stars(&self) -> f64 {
        self.attributes.stars()
    }
}

#[inline(always)]
pub fn mode_any_pp(mode: Option<u8>, beatmap: &RawBeatmap) -> AnyPP {
    match mode {
        Some(m) => match m {
            0 => AnyPP::Osu(OsuPP::new(beatmap)),
            1 => AnyPP::Taiko(TaikoPP::new(beatmap)),
            2 => AnyPP::Catch(CatchPP::new(beatmap)),
            3 => AnyPP::Mania(ManiaPP::new(beatmap)),
            _ => AnyPP::new(beatmap),
        },
        None => AnyPP::new(beatmap),
    }
}
