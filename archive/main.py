""" get camera with onvif """
import cv2 as cv
from onvif import ONVIFCamera


def media_profile_configuration():
    '''
    A media profile consists of configuration entities such as video/audio
    source configuration, video/audio encoder configuration,
    or PTZ configuration. This use case describes how to change one
    configuration entity which has been already added to the media profile.
    '''

    # Create the media service
    mycam = ONVIFCamera('172.16.18.151', 80 , 'admin', '123456')
    media_service = mycam.create_media_service()

    profiles = media_service.GetProfiles()
    # print(f'Profiles: {profiles}')
    print(f"profiles[0].token: {profiles[0].token}")

    # Use the first profile and Profiles have at least one
    token = profiles[0].token

    # Get all video encoder configurations
    configurations_list = media_service.GetVideoEncoderConfigurations()
    # print(f'configuration list: {configurations_list}')
    # Use the first profile and Profiles have at least one
    video_encoder_configuration = configurations_list[0]
    print(f'\nvideo_encoder_configuration: {video_encoder_configuration}')

    # Get video encoder configuration options
    options = media_service.GetVideoEncoderConfigurationOptions({'ProfileToken':token})
    print(f'Options: {options}')
     # Setup stream configuration
    video_encoder_configuration.Encoding = 'H264'
     # Setup Resolution
    video_encoder_configuration.Resolution.Width = \
                    options.H264.ResolutionsAvailable[0].Width
    video_encoder_configuration.Resolution.Height = \
                    options.H264.ResolutionsAvailable[0].Height
    # Setup Quality
    video_encoder_configuration.Quality = options.QualityRange.Max
    # Setup FramRate
    video_encoder_configuration.RateControl.FrameRateLimit = \
                                    options.H264.FrameRateRange.Max
    # Setup EncodingInterval
    video_encoder_configuration.RateControl.EncodingInterval = \
                                    options.H264.EncodingIntervalRange.Min
    # Setup Bitrate
    # video_encoder_configuration.RateControl.BitrateLimit = \
                            # options.Extension.H264[0].BitrateRange[0].Min[0]

    # Create request type instance
    request = media_service.create_type('SetVideoEncoderConfiguration')
    request.Configuration = video_encoder_configuration
    # ForcePersistence is obsolete and should always be assumed to be True
    request.ForcePersistence = True

    # Set the video encoder configuration
    media_service.SetVideoEncoderConfiguration(request)

    return (media_service, token)

def get_rtsp(media_service, token):
    """ get the URI for the stream using RTSP """
    stream_setup = {'StreamSetup' : 
                        { 'Stream' : 'RTP_unicast', 
                          'Transport' : { 'Protocol' : 'UDP' } 
                          }, 
                        'ProfileToken' : token}
    uri = media_service.GetStreamUri(stream_setup)
    rtsp_stream = uri.Uri
    print(f'uri: {uri.Uri}')
    return rtsp_stream

def fetch_video(rtsp_stream):
    """Display the video"""
    capture = cv.VideoCapture(rtsp_stream)
    while capture.isOpened():

        ret, frame = capture.read()
        if ret:
            cv.imshow('capturing ', frame)           

        if cv.waitKey(1) & 0xFF == ord('q') or cv.waitKey(1) == 27:
            cv.destroyAllWindows()
            break

    capture.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    media_service, token = media_profile_configuration()
    rtsp_stream = get_rtsp(media_service, token)
    fetch_video(rtsp_stream)

    