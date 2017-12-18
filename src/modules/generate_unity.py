# Generate Unity assets

def generate_unity (palette, filename):
    f = open(filename, 'w')

    f.write('%YAML 1.1\n')
    f.write('%TAG !u! tag:unity3d.com,2011:\n')
    f.write('--- !u!114 &1\n')
    f.write('MonoBehaviour:\n')
    f.write('  m_ObjectHideFlags: 52\n')
    f.write('  m_PrefabParentObject: {fileID: 0}\n')
    f.write('  m_PrefabInternal: {fileID: 0}\n')
    f.write('  m_GameObject: {fileID: 0}\n')
    f.write('  m_Enabled: 1\n')
    f.write('  m_EditorHideFlags: 1\n')
    f.write('  m_Script: {fileID: 12323, guid: 0000000000000000e000000000000000, type: 0}\n')
    f.write('  m_Name: ' + palette['name'] + '\n')
    f.write('  m_EditorClassIdentifier: \n')
    f.write('  m_Presets:\n')

    for color in palette['colors']:
        f.write('  - m_Name: "' + color[3] + '"\n')
        f.write('    m_Color: {r: %.8g, g: %.8g, b: %.8g, a: 1}\n' % tuple(map(lambda x: x/255.0, color[:3])))
        
    f.close()
