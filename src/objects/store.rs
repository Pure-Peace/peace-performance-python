// Experminal design

#[pyclass]
pub struct BeatmapCache {
    pub beatmap: Beatmap,
    pub access: usize,
    pub create_time: DateTime<Local>,
    pub last_access: DateTime<Local>,
}

impl BeatmapCache {
    pub fn new(beatmap: Beatmap) -> Self {
        Self {
            beatmap,
            access: 0,
            create_time: Local::now(),
            last_access: Local::now(),
        }
    }

    #[inline(always)]
    pub fn get(&mut self) -> &Beatmap {
        self.access += 1;
        self.last_access = Local::now();
        &self.beatmap
    }
}

type StoreSpace<T> = HashMap<T, BeatmapRef>;
type BeatmapRef = Rc<RefCell<BeatmapCache>>;

#[pyclass]
pub struct BeatmapStore {
    pub md5: StoreSpace<String>,
    pub bid: StoreSpace<u32>,
    pub limit: usize,
}

impl BeatmapStore {
    pub fn new(limit: usize) -> Self {
        Self {
            md5: HashMap::with_capacity(limit),
            bid: HashMap::with_capacity(limit),
            limit,
        }
    }

    #[inline(always)]
    pub fn store(&mut self, md5: Option<&str>, bid: Option<u32>, beatmap: BeatmapRef) {
        if let Some(md5) = md5 {
            self.store_with_md5(md5, beatmap)
        }

        if let Some(bid) = bid {
            self.store_with_bid(bid, beatmap)
        }
    }

    #[inline(always)]
    fn store_with_md5(&mut self, md5: &str, beatmap: BeatmapRef) {
        self.md5.insert(md5.into(), beatmap);
    }

    #[inline(always)]
    fn store_with_bid(&mut self, bid: u32, beatmap: BeatmapRef) {
        self.bid.insert(bid, beatmap);
    }
}
