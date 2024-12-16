import { defineEventHandler, readMultipartFormData } from "h3";
import Sharp from "sharp";
import { join } from "path";
import { mkdir } from "fs/promises";
import { useTurso } from "~/lib/turso";

export default defineEventHandler(async (event) => {
  try {
    const formData = await readMultipartFormData(event);

    if (!formData) {
      throw createError({
        statusCode: 400,
        message: "Keine Formulardaten empfangen",
      });
    }

    const imageFile = formData.find((item) => item.name === "image");
    const userId = formData.find((item) => item.name === "userId");

    if (!imageFile || !userId) {
      throw createError({
        statusCode: 400,
        message: "Bild oder UserId fehlt",
      });
    }

    const uploadDir = join(process.cwd(), "public", "uploads", "profile");
    await mkdir(uploadDir, { recursive: true });

    const fileName = `profile-${userId.data.toString()}-${Date.now()}.webp`;
    const filePath = join(uploadDir, fileName);
    const imageUrl = `/uploads/profile/${fileName}`;

    await Sharp(imageFile.data)
      .resize(200, 200, {
        fit: "cover",
        position: "center",
      })
      .webp({ quality: 80 })
      .toFile(filePath);

    const db = useTurso();
    await db.execute({
      sql: "UPDATE user SET image = ? WHERE id = ?",
      args: [imageUrl, userId.data.toString()],
    });

    return { imageUrl };
  } catch (error) {
    console.error("Fehler beim Bildupload:", error);
    throw createError({
      statusCode: 500,
      message: `Fehler beim Bildupload: ${error.message}`,
    });
  }
});
