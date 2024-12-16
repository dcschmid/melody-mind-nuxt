import { defineEventHandler, readMultipartFormData } from "h3";
import Sharp from "sharp";
import { join } from "path";
import { mkdir } from "fs/promises";
import { useTurso } from "~/lib/turso";

export default defineEventHandler(async (event) => {
  try {
    const formData = await readMultipartFormData(event);
    const imageFile = formData?.find((item) => item.name === "profileImage");
    const userId = formData?.find((item) => item.name === "userId")?.data.toString();

    if (!imageFile || !userId) {
      throw createError({
        statusCode: 400,
        message: "Bild oder UserId fehlt",
      });
    }

    const uploadDir = join(process.cwd(), "public", "uploads", "profile");
    await mkdir(uploadDir, { recursive: true });

    const fileName = `profile-${userId}-${Date.now()}.webp`;
    const filePath = join(uploadDir, fileName);
    const imageUrl = `/uploads/profile/${fileName}`;

    await Sharp(imageFile.data)
      .resize(300, 300, {
        fit: "cover",
        position: "center",
      })
      .webp({ quality: 80 })
      .toFile(filePath);

    const db = useTurso();
    await db.execute({
      sql: "UPDATE user SET image = ? WHERE id = ?",
      args: [imageUrl, userId],
    });

    return { imageUrl };
  } catch (error) {
    console.error("Fehler beim Bildupload:", error);
    throw createError({
      statusCode: 500,
      message: "Fehler beim Bildupload",
    });
  }
});
