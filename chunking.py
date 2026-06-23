#this was basically a character based chunking with overlap
"""
def chunking(input1,chunk_size,overlap):
    start = 0
    end = chunk_size
    step = chunk_size - overlap
    chunks = []
    lenght = len(input1)
    text = input1.split()
    print(len(text))
    print(lenght)
    while start < lenght:
        chunks.append(input1[start:end] + "\n")
        print(input1[start:end] + "\n"+ "\n")
        start = start + step
        end = start + chunk_size
    return chunks

       
input1 = "The sun hung low over the rolling hills, casting long shadows that stretched like dark fingers across the meadow. A gentle breeze carried the scent of wildflowers and freshly turned earth, stirring the tall grass into waves of green and gold. In the distance, a small farmhouse sat nestled among ancient oak trees, its whitewashed walls glowing warmly in the fading light. Smoke curled lazily from the stone chimney, promising a cozy fire within against the evening chill. The farmer, a grizzled man named Ezra, leaned against his wooden fence, chewing on a piece of straw as he watched the sky turn from blue to orange to deep crimson. He had worked this land for forty years, through droughts and floods, through good harvests and lean ones. His hands were rough and calloused, his face weathered like old leather, but his eyes still held the same spark of wonder they had when he was a boy. He remembered his father telling him that the land was not something you owned, but something you borrowed from your children. Those words had guided every decision he ever made. He rotated his crops carefully, let his fields lie fallow when they needed rest, and planted more trees than he ever cut down. His neighbors thought he was old-fashioned, but Ezra knew that nature repaid patience with abundance. As the first stars began to appear, a flock of geese flew overhead in perfect V-formation, their distant honking echoing across the valley. Ezra smiled and pushed off from the fence, walking slowly back toward the house. His wife, Martha, would have supper ready by now—a hearty stew with fresh bread and butter. Inside, the kitchen was warm and smelled of rosemary and garlic. Their old border collie, Rusty, wagged his tail lazily from his spot by the stove. Ezra hung his hat on the hook by the door and sat down at the wooden table, worn smooth by decades of family meals. Martha placed a steaming bowl in front of him and kissed his forehead. They ate in comfortable silence, the way old couples do, listening to the crackling fire and the soft whistle of the wind outside. After supper, Ezra would mend his leather harness by the fire, and Martha would read her worn-out romance novel, its pages yellowed and fragile. It was a simple life, but it was theirs. And as the moon rose high above the hills, casting its silver light over the sleeping fields, Ezra felt a deep and quiet peace settle over his heart. He knew that tomorrow would bring its own challenges, but tonight, all was well."
chunk_size= 100
overlap = 20
output = chunking(input1,chunk_size,overlap)
"""

#this is word based chunking with overlap


def word_chunking(text,chunk_size,overlap):
    step = chunk_size - overlap
    start = 0
    text = text.split(" ")
    end = chunk_size
    chunks = []
    lenght = len(text)
    while start < lenght:
        chunk = text[start:end]
        new_chunk = []
        l = len(chunk)
        new_chunk = []
        for i in range(l):
            new_chunk.append(chunk[i])
        updated_chunk = " ".join(new_chunk)
        chunks.append(updated_chunk)

        start = start + step
        end = start + chunk_size

    return chunks

"""
chunk_size = 100
overlap = 20
text = "The sun hung low over the rolling hills, casting long shadows that stretched like dark fingers across the meadow. A gentle breeze carried the scent of wildflowers and freshly turned earth, stirring the tall grass into waves of green and gold. In the distance, a small farmhouse sat nestled among ancient oak trees, its whitewashed walls glowing warmly in the fading light. Smoke curled lazily from the stone chimney, promising a cozy fire within against the evening chill. The farmer, a grizzled man named Ezra, leaned against his wooden fence, chewing on a piece of straw as he watched the sky turn from blue to orange to deep crimson. He had worked this land for forty years, through droughts and floods, through good harvests and lean ones. His hands were rough and calloused, his face weathered like old leather, but his eyes still held the same spark of wonder they had when he was a boy. He remembered his father telling him that the land was not something you owned, but something you borrowed from your children. Those words had guided every decision he ever made. He rotated his crops carefully, let his fields lie fallow when they needed rest, and planted more trees than he ever cut down. His neighbors thought he was old-fashioned, but Ezra knew that nature repaid patience with abundance. As the first stars began to appear, a flock of geese flew overhead in perfect V-formation, their distant honking echoing across the valley. Ezra smiled and pushed off from the fence, walking slowly back toward the house. His wife, Martha, would have supper ready by now—a hearty stew with fresh bread and butter. Inside, the kitchen was warm and smelled of rosemary and garlic. Their old border collie, Rusty, wagged his tail lazily from his spot by the stove. Ezra hung his hat on the hook by the door and sat down at the wooden table, worn smooth by decades of family meals. Martha placed a steaming bowl in front of him and kissed his forehead. They ate in comfortable silence, the way old couples do, listening to the crackling fire and the soft whistle of the wind outside. After supper, Ezra would mend his leather harness by the fire, and Martha would read her worn-out romance novel, its pages yellowed and fragile. It was a simple life, but it was theirs. And as the moon rose high above the hills, casting its silver light over the sleeping fields, Ezra felt a deep and quiet peace settle over his heart. He knew that tomorrow would bring its own challenges, but tonight, all was well."
output = word_chunking(text,chunk_size,overlap)
print(output)
"""