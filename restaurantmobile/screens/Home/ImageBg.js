import { ImageBackground, View } from "react-native";
import HomeStyle from "../../styles/HomeStyle";

const ImageBg = () => {
    return(
        <View style={{ alignItems: "center" }}>
                <ImageBackground source={{uri: 'https://res.cloudinary.com/dx4i4a03w/image/upload/v1767532810/bgnhahang_ycrnnl.png'}}
                                        style={HomeStyle.banner}
                                        imageStyle={HomeStyle.bannerImage}
                                        resizeMode="cover" />
        </View>
    )
} 

export default ImageBg;