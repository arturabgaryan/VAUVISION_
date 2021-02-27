const SONG_DESCRIPTION_FIELDS = [
    ['melodyAuthor', ''],
    ['textAuthor', ''],
    ['artist', ''],
];

const getSongDefaultDescription = ({
                                       name
                                   }) => {
    return {
        name,

        ...Object.fromEntries(SONG_DESCRIPTION_FIELDS)
    };
};
var app = new Vue({
    el: '#app',
    data: {
        releaseType: null,
        filthy: false,
        filthyTracks: '',
        passportScans: null,
        infoSource: null,
        releaseName: '',
        songs: {
            songsDescriptonsList: [],
            songsList: [],
            songDescriptionFieldsNames: SONG_DESCRIPTION_FIELDS.map(
                ([fieldName]) => fieldName
            )
        },
        videoCheck: false,
        pickerOptions: {
            disabledDate(time) {
                return time.getTime() > Date.now();
            },
            shortcuts: [{
                text: 'Today',
                onClick(picker) {
                    picker.$emit('pick', new Date());
                }
            }]
        },
        value1: '',

    },
    methods: {
        handleFileUpload() {
            this.passportScans = this.$refs.files.files
        }
        ,
        handleFileUploadMusic(event) {
            console.log(event);
            const songsFilesList = Array.from(event.target.files);

            this.songs.songsList = songsFilesList;
            this.songs.songsDescriptonsList = songsFilesList.map(getSongDefaultDescription);
        }
        ,
        changeTrack: function (id) {
            let text = document.querySelector(`#new_track_name_${id}`).value
            axios
                .get('http://127.0.0.1:8000/form-admin/change-track-name/?id=${id}&name=${text}')
                .then(location.reload())
        }

    }
});
