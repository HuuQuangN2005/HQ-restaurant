import { StyleSheet } from "react-native";

export default StyleSheet.create({
  container: {
    flex: 1
  },

  title: {
    fontSize: 30,
    fontWeight: "bold",
    color: "blue",
    alignSelf: "center"
  },

  row: {
    flexDirection: "row",
    flexWrap: "wrap",
  },

  margin: {
    margin: 20
  },
  
  padding: {
    padding: 8
  },
  
  goBack: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#000",
    paddingHorizontal: 12,
    paddingVertical: 6,
  }
});